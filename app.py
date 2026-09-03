import streamlit as st
import pandas as pd
import plotly.express as px
import os


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="MoneyTrack AI",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# SIDEBAR FONT SIZE
# --------------------------------------------------

st.markdown("""
<style>
[data-testid="stSidebar"] {
    width: 280px !important;
}

[data-testid="stSidebar"] {
    font-size: 18px;
}

[data-testid="stSidebar"] label {
    font-size: 18px !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 22px !important;
}

</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💰 MoneyTrack AI")

st.write(
    "AI-powered personal finance dashboard — "
    "understand, track and plan your money."
)



# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("💰 MoneyTrack AI")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "📊 Dashboard",
        "💳 Transactions",
        "📈 Predictions",
        "🧠 AI Advisor",
        "🎯 Goal Planner",
        "🔮 What-If Simulator"
    ]
)




# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------


df = pd.read_csv(
    "data/sample_transactions.csv",
    encoding="utf-8-sig"
)

df.columns = (
    df.columns
    .str.strip()
    .str.replace("\ufeff", "", regex=False)
)

df["Date"] = pd.to_datetime(df["Date"])


def categorize_transaction(description):

    description = str(description).lower().strip()

    # Food
    if any(word in description for word in [
        "swiggy", "zomato", "restaurant", "pizza",
        "food", "dominos", "mcdonald", "kfc",
        "burger", "cafe", "starbucks"
    ]):
        return "Food"

    # Shopping
    elif any(word in description for word in [
        "amazon", "flipkart", "myntra", "shopping",
        "mall", "retail", "ajio", "meesho"
    ]):
        return "Shopping"

    # Transport
    elif any(word in description for word in [
        "uber", "ola", "petrol", "fuel", "metro",
        "bus", "train", "irctc", "rapido"
    ]):
        return "Transport"

    # Bills
    elif any(word in description for word in [
        "electricity", "water", "internet", "wifi",
        "mobile", "recharge", "bill", "jio",
        "airtel", "vi"
    ]):
        return "Bills"

    # Entertainment
    elif any(word in description for word in [
        "netflix", "spotify", "movie", "cinema",
        "prime", "youtube", "hotstar", "gaming"
    ]):
        return "Entertainment"

    # Health
    elif any(word in description for word in [
        "hospital", "medical", "medicine", "pharmacy",
        "doctor", "clinic", "apollo", "health"
    ]):
        return "Health"

    # Education
    elif any(word in description for word in [
        "college", "school", "course", "udemy",
        "coursera", "education", "book", "library"
    ]):
        return "Education"

    # Rent / Housing
    elif any(word in description for word in [
        "rent", "housing", "maintenance", "property"
    ]):
        return "Housing"

    # Income
    elif any(word in description for word in [
        "salary", "income", "credited", "deposit"
    ]):
        return "Income"

    else:
        return "Other"


df["Category"] = df["Description"].apply(
    categorize_transaction
)




# --------------------------------------------------
# FINANCIAL METRICS
# --------------------------------------------------

total_income = df.loc[
    df["Type"] == "Income",
    "Amount"
].sum()

total_expense = df.loc[
    df["Type"] == "Expense",
    "Amount"
].sum()

total_savings = total_income - total_expense

if total_income > 0:
    savings_rate = (
        total_savings / total_income
    ) * 100
else:
    savings_rate = 0




category_expense = (
    df[df["Type"] == "Expense"]
    .groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

top_category = category_expense.loc[
    category_expense["Amount"].idxmax(),
    "Category"
]

top_category_amount = category_expense["Amount"].max()




# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "📊 Dashboard":

    # Financial Overview
    st.header("📊 Financial Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "💰 Total Income",
        f"₹{total_income:,.0f}"
    )

    col2.metric(
        "💸 Total Expenses",
        f"₹{total_expense:,.0f}"
    )

    col3.metric(
        "🏦 Total Savings",
        f"₹{total_savings:,.0f}"
    )

    col4.metric(
        "📊 Savings Rate",
        f"{savings_rate:.1f}%"
    )

    col5.metric(
        "🔥 Top Spending",
        top_category,
        f"₹{top_category_amount:,.0f}"
    )



# ----------------------------------------------
    # SPENDING BY CATEGORY
    # ----------------------------------------------

    st.subheader("💸 Spending by Category")

    fig_category = px.bar(
        category_expense,
        x="Category",
        y="Amount",
        title="Expenses by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


    # ----------------------------------------------
    # SPENDING DISTRIBUTION
    # ----------------------------------------------

    st.subheader("🥧 Spending Distribution")

    fig_pie = px.pie(
        category_expense,
        names="Category",
        values="Amount",
        hole=0.45,
        title="Spending Distribution"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )





# --------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------

elif page == "💳 Transactions":

    st.header("💳 Transactions")

    st.write(
        "View and filter all your financial transactions."
    )

    # ----------------------------------------------
    # TRANSACTION SUMMARY
    # ----------------------------------------------

    total_transactions = len(df)

    income_transactions = len(
        df[df["Type"] == "Income"]
    )

    expense_transactions = len(
        df[df["Type"] == "Expense"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📋 Total Transactions",
        total_transactions
    )

    col2.metric(
        "💰 Income Transactions",
        income_transactions
    )

    col3.metric(
        "💸 Expense Transactions",
        expense_transactions
    )

    # ----------------------------------------------
    # SEARCH
    # ----------------------------------------------

    search = st.text_input(
        "🔍 Search transaction",
        placeholder="Example: Amazon, Food, Salary..."
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df["Description"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # ----------------------------------------------
    # CATEGORY FILTER
    # ----------------------------------------------

    categories = ["All"] + sorted(
        df["Category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "📂 Filter by Category",
        categories
    )

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    # ----------------------------------------------
    # TYPE FILTER
    # ----------------------------------------------

    transaction_types = [
        "All",
        "Income",
        "Expense"
    ]

    selected_type = st.selectbox(
        "💰 Filter by Type",
        transaction_types
    )

    if selected_type != "All":

        filtered_df = filtered_df[
            filtered_df["Type"] == selected_type
        ]

    # ----------------------------------------------
    # DISPLAY TRANSACTIONS
    # ----------------------------------------------

    st.subheader("📋 Transaction History")

    st.dataframe(
        filtered_df[
            [
                "Date",
                "Description",
                "Amount",
                "Type",
                "Category"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )







    # ----------------------------------------------
    # SPENDING BY CATEGORY
    # ----------------------------------------------

    st.subheader("💸 Spending by Category")

    fig = px.bar(
        category_expense,
        x="Category",
        y="Amount",
        title="Expenses by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # ----------------------------------------------
    # SPENDING DISTRIBUTION
    # ----------------------------------------------

    st.subheader("🥧 Spending Distribution")

    fig_pie = px.pie(
        category_expense,
        names="Category",
        values="Amount",
        hole=0.45
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# ----------------------------------------------
# ML PREDICTIONS
# ----------------------------------------------

elif page == "📈 Predictions":

    st.header("🤖 ML Predictions")

    st.write(
        "Machine Learning models analyze your financial "
        "behavior and provide predictive insights."
    )

    # ----------------------------------------------
    # LOAD ML DATA
    # ----------------------------------------------

    st.subheader("📈 Expense Forecast")

    monthly_ml = pd.read_csv(
        "C:/Users/yashl/OneDrive/Desktop/Moneytrack AI/data/financial_history.csv"
    )

    monthly_ml["Month"] = pd.to_datetime(
        monthly_ml["Month"]
    )

    # Create month number
    monthly_ml["Month_Number"] = range(
        1,
        len(monthly_ml) + 1
    )

    # ----------------------------------------------
    # PREPARE DATA
    # ----------------------------------------------

    x = monthly_ml[["Month_Number"]]

    y = monthly_ml["Expense"]

    # ----------------------------------------------
    # TRAIN MODEL 1
    # ----------------------------------------------

    from sklearn.linear_model import LinearRegression

    expense_model = LinearRegression()

    expense_model.fit(x, y)

    # ----------------------------------------------
    # PREDICT NEXT MONTH
    # ----------------------------------------------

    next_month = len(monthly_ml) + 1

    predicted_expense = expense_model.predict(
        [[next_month]]
    )[0]

    # ----------------------------------------------
    # SHOW PREDICTION
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    col1.metric(
        "💸 Predicted Next Month Expense",
        f"₹{predicted_expense:,.0f}"
    )

    col2.metric(
        "📅 Forecast Month",
        f"Month {next_month}"
    )

    # ----------------------------------------------
    # HISTORICAL DATA
    # ----------------------------------------------

    st.subheader("📊 Expense Forecast Trend")

    fig_forecast = px.line(
        monthly_ml,
        x="Month",
        y="Expense",
        markers=True,
        title="Monthly Expense Trend"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    # ----------------------------------------------
    # SHOW DATA
    # ----------------------------------------------

    st.subheader("📋 Historical ML Data")

    st.dataframe(
        monthly_ml,
        use_container_width=True
    )






    # ----------------------------------------------
    # MODEL 2 - SAVINGS HEALTH
    # ----------------------------------------------

    st.subheader("🏦 Savings Health")

    # Calculate current savings rate

    current_savings_rate = savings_rate

    # Classify financial health

    if current_savings_rate >= 30:
        savings_health = "Excellent"

    elif current_savings_rate >= 20:
        savings_health = "Good"

    elif current_savings_rate >= 10:
        savings_health = "Average"

    else:
        savings_health = "Poor"

    # Display result

    col1, col2 = st.columns(2)

    col1.metric(
        "📊 Current Savings Rate",
        f"{current_savings_rate:.1f}%"
    )

    col2.metric(
        "🏦 Savings Health",
        savings_health
    )





elif page == "🧠 AI Advisor":

    st.header("🧠 AI Financial Advisor")

    st.write(
        "Ask questions about your spending, savings and "
        "financial habits."
    )

    # ----------------------------------------------
    # FINANCIAL SUMMARY FOR AI
    # ----------------------------------------------

    financial_summary = f"""
    Total Income: ₹{total_income:,.0f}
    Total Expenses: ₹{total_expense:,.0f}
    Total Savings: ₹{total_savings:,.0f}
    Savings Rate: {savings_rate:.1f}%
    Top Spending Category: {top_category}
    Top Category Spending: ₹{top_category_amount:,.0f}
    """

    user_question = st.text_area(
        "💬 Ask your financial question",
        placeholder="Example: How can I reduce my expenses?"
    )


    if st.button("🤖 Get AI Advice"):

        if user_question:

            try:

                from google import genai

                client = genai.Client()

                prompt = f"""
You are MoneyTrack AI, a personal finance advisor.

Here is the user's financial information:

{financial_summary}

The user's question is:

{user_question}

Give practical and personalized financial advice.

Rules:
- Use the actual financial numbers.
- Keep the explanation simple.
- Give 2 or 3 practical actions.
- Do not invent financial information.
- Do not guarantee financial returns.
"""

                response = client.models.generate_content(
                   model="gemini-3.6-flash",
                   contents=prompt
                )

                st.subheader("💡 AI Advice")

                st.write(response.text)

            except Exception as e:

                st.error(
                    f"AI Error: {e}"
                )

        else:

            st.warning(
                "Please enter a question first."
            )

    # --------------------------------------------------
# WHAT-IF SIMULATOR
# --------------------------------------------------

elif page == "🔮 What-If Simulator":

    st.header("🔮 What-If Financial Simulator")

    st.write(
        "Simulate different financial decisions and see "
        "how they affect your savings."
    )

    # ----------------------------------------------
    # CHOOSE SCENARIO
    # ----------------------------------------------

    scenario = st.selectbox(
        "🔮 Choose a scenario",
        [
            "💸 Reduce Expenses",
            "💰 Increase Income",
            "🎯 Increase Savings Target"
        ]
    )


    # ==================================================
    # OPTION 1 - REDUCE EXPENSES
    # ==================================================

    if scenario == "💸 Reduce Expenses":

        reduction = st.number_input(
            "💸 How much expense do you want to reduce?",
            min_value=0.0,
            max_value=float(total_expense),
            value=5000.0,
            step=500.0
        )

        new_income = total_income

        new_expense = total_expense - reduction

        new_savings = new_income - new_expense

        if new_income > 0:

            new_savings_rate = (
                new_savings / new_income
            ) * 100

        else:

            new_savings_rate = 0


        st.subheader("📊 Simulation Result")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💸 New Expenses",
            f"₹{new_expense:,.0f}",
            f"-₹{reduction:,.0f}"
        )

        col2.metric(
            "🏦 New Savings",
            f"₹{new_savings:,.0f}",
            f"+₹{reduction:,.0f}"
        )

        col3.metric(
            "📈 New Savings Rate",
            f"{new_savings_rate:.1f}%",
            f"+{new_savings_rate - savings_rate:.1f}%"
        )


    # ==================================================
    # OPTION 2 - INCREASE INCOME
    # ==================================================

    elif scenario == "💰 Increase Income":

        income_increase = st.number_input(
            "💰 How much additional income do you expect?",
            min_value=0.0,
            value=10000.0,
            step=1000.0
        )

        new_income = total_income + income_increase

        new_expense = total_expense

        new_savings = new_income - new_expense

        if new_income > 0:

            new_savings_rate = (
                new_savings / new_income
            ) * 100

        else:

            new_savings_rate = 0


        st.subheader("📊 Simulation Result")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 New Income",
            f"₹{new_income:,.0f}",
            f"+₹{income_increase:,.0f}"
        )

        col2.metric(
            "🏦 New Savings",
            f"₹{new_savings:,.0f}",
            f"+₹{income_increase:,.0f}"
        )

        col3.metric(
            "📈 New Savings Rate",
            f"{new_savings_rate:.1f}%",
            f"{new_savings_rate - savings_rate:+.1f}%"
        )


    # ==================================================
    # OPTION 3 - INCREASE SAVINGS TARGET
    # ==================================================

    elif scenario == "🎯 Increase Savings Target":

        target_savings = st.number_input(
            "🎯 What monthly savings do you want to achieve?",
            min_value=0.0,
            value=120000.0,
            step=5000.0
        )

        additional_required = (
            target_savings - total_savings
        )

        target_savings_rate = (
            target_savings / total_income
        ) * 100 if total_income > 0 else 0


        st.subheader("📊 Savings Goal Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🏦 Current Savings",
            f"₹{total_savings:,.0f}"
        )

        col2.metric(
            "🎯 Target Savings",
            f"₹{target_savings:,.0f}"
        )

        col3.metric(
            "📈 Target Savings Rate",
            f"{target_savings_rate:.1f}%"
        )


        if additional_required > 0:

            st.warning(
                f"You need ₹{additional_required:,.0f} "
                "more savings to reach this target."
            )

        else:

            st.success(
                "🎉 You are already above this savings target!"
            )





        # ----------------------------------------------
    # AI SCENARIO ANALYSIS
    # ----------------------------------------------

    if st.button("🤖 Analyze This Scenario"):

        try:

            from google import genai

            client = genai.Client()

            prompt = f"""
You are MoneyTrack AI, a personal finance advisor.

Analyze this what-if financial scenario.

Current financial situation:
Income: ₹{total_income:,.0f}
Current Expenses: ₹{total_expense:,.0f}
Current Savings: ₹{total_savings:,.0f}
Current Savings Rate: {savings_rate:.1f}%

The user wants to reduce expenses by:
₹{reduction:,.0f}

After reducing expenses:

New Expenses: ₹{new_expense:,.0f}
New Savings: ₹{new_savings:,.0f}
New Savings Rate: {new_savings_rate:.1f}%

Explain in simple language:

1. How much additional money the user saves.
2. How the savings rate changes.
3. Whether this is a good improvement.
4. Give 2 practical suggestions.

Use only the numbers provided.
Do not invent financial information.
Do not guarantee investment returns.
"""

            with st.spinner("🤖 AI is analyzing your scenario..."):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            st.subheader("🧠 AI Scenario Analysis")

            st.success("Scenario analyzed successfully!")

            st.write(response.text)

        except Exception as e:

            st.error(f"AI Error: {e}")


            # --------------------------------------------------
# GOAL PLANNER
# --------------------------------------------------

elif page == "🎯 Goal Planner":

    st.header("🎯 AI Financial Goal Planner")

    st.write(
        "Set a financial goal and get a personalized savings plan."
    )

    # ----------------------------------------------
    # GOAL INPUT
    # ----------------------------------------------

    goal_name = st.text_input(
        "🎯 What are you saving for?",
        placeholder="Example: Laptop"
    )

    target_amount = st.number_input(
        "💰 Target Amount (₹)",
        min_value=0.0,
        value=50000.0,
        step=5000.0
    )

    months = st.number_input(
        "📅 How many months do you have?",
        min_value=1,
        value=6,
        step=1
    )

    # ----------------------------------------------
    # CALCULATE MONTHLY TARGET
    # ----------------------------------------------

    monthly_required = target_amount / months

    # ----------------------------------------------
    # SHOW GOAL CALCULATION
    # ----------------------------------------------

    st.subheader("📊 Goal Calculation")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎯 Goal Amount",
        f"₹{target_amount:,.0f}"
    )

    col2.metric(
        "📅 Time",
        f"{months} months"
    )

    col3.metric(
        "💰 Required Monthly Saving",
        f"₹{monthly_required:,.0f}"
    )

    # ----------------------------------------------
    # AI GOAL ANALYSIS
    # ----------------------------------------------

    if st.button("🤖 Create My AI Savings Plan"):

        if goal_name:

            try:

                from google import genai

                client = genai.Client()

                prompt = f"""
You are MoneyTrack AI, a personal finance planning assistant.

Create a simple savings plan for the user's financial goal.

User's goal:
{goal_name}

Target amount:
₹{target_amount:,.0f}

Time available:
{months} months

Required monthly saving:
₹{monthly_required:,.0f}

Current financial situation:
Income: ₹{total_income:,.0f}
Expenses: ₹{total_expense:,.0f}
Current Savings: ₹{total_savings:,.0f}
Savings Rate: {savings_rate:.1f}%

Explain:

1. How much the user needs to save each month.
2. Whether this monthly target looks manageable based on their current savings.
3. Give 3 practical suggestions to reach the goal.
4. Mention the user's current savings rate.
5. Keep the answer simple and realistic.

Do not invent financial information.
Do not guarantee investment returns.
"""

                with st.spinner(
                    "🤖 AI is creating your savings plan..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                st.subheader("🧠 Your AI Savings Plan")

                st.success(
                    f"Plan created for your goal: {goal_name}"
                )

                st.write(response.text)

            except Exception as e:

                st.error(
                    f"AI Error: {e}"
                )

        else:

            st.warning(
                "Please enter a goal name first."
            )