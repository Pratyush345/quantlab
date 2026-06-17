import streamlit as st
from enum import Enum
from datetime import datetime, timedelta
import yfinance as yf
from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel, Ticker
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class OPTION_PRICING_MODEL(Enum):
    HOME = "Home"
    BLACK_SCHOLES = 'Black-Scholes Pricing'
    MONTE_CARLO = 'Monte Carlo Pricing'
    BINOMIAL = 'Binomial Tree Pricing'
    PAYOFF = "Strategy Analytics Dashboard"
    COMPARISON = "Model Comparison Dashboard"

@st.cache_data
def get_historical_data(ticker):
    try:
        data = Ticker.get_historical_data(ticker)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

@st.cache_data

def get_current_price(ticker):
    return 100.0

# Ignore the Streamlit warning for using st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.title("📊 QuantLab")
st.sidebar.markdown("---")

# User selected model from sidebar 
pricing_method = st.sidebar.radio("Select Module", options=[model.value for model in OPTION_PRICING_MODEL])

# Displaying specified model
if pricing_method != OPTION_PRICING_MODEL.HOME.value:
    st.header(f"Pricing method: {pricing_method}")

if pricing_method == OPTION_PRICING_MODEL.HOME.value:

    st.title("QuantLab")
    st.caption(
    "Interactive platform for option pricing, strategy analytics, and quantitative model comparison"
    )
    st.subheader("Key Capabilities")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pricing Models", "3", "Implemented")

    with col2:
        st.metric("Strategies", "4", "Supported")

    with col3:
        st.metric("Dashboards", "2", "Available")

    st.subheader("Platform Features")
    

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    ### 📈 Pricing Models

    - Black-Scholes Pricing
    - Monte Carlo Pricing
    - Binomial Tree Pricing
    """)

    with col2:
        st.markdown("""
    ### 📊 Analytics & Visualization

    - Strategy Analytics
    - Model Comparison Dashboard
    - Interactive Visualizations
    """)
    st.info(
    """
    Compare option pricing models, analyze trading strategies,
    and visualize quantitative finance concepts in one platform.
    """
    )

if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    # Parameters for Black-Scholes model
    spot_price = st.number_input(
    "Spot Price",
    min_value=1.0,
    value=100.0
    )
    # Fetch current price
    current_price = spot_price
    
    if current_price is not None:
        st.metric("Current Spot Price", f"${current_price:.2f}")
        
        # Set default and min/max values based on current price
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption(
        f"The price at which the option can be exercised. Suggested range: ${min_strike:.2f} to ${max_strike:.2f}"
        )

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")
    
    if st.button("Calculate Option Price"):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data("AAPL")

            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, "Demo Data", 'Close')
                st.pyplot(fig)

                spot_price = Ticker.get_last_price(data, 'Close')
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
                call_option_price = BSM.calculate_option_price('Call Option')
                put_option_price = BSM.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")

elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    # Parameters for Monte Carlo simulation
    spot_price = st.number_input(
    "Spot Price",
    min_value=1.0,
    value=100.0
    )
    

    # Fetch current price
    current_price = spot_price
    
    if current_price is not None:
        st.metric("Current Spot Price", f"${current_price:.2f}")
        
        # Set default and min/max values based on current price
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption(
        f"The price at which the option can be exercised. Suggested range: ${min_strike:.2f} to ${max_strike:.2f}"
        )

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")

    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    st.caption("The number of price paths to simulate. More simulations increase accuracy but take longer to compute.")

    num_of_movements = st.slider('Number of price movement simulations to be visualized ', 0, int(number_of_simulations/10), 100)
    st.caption("The number of simulated price paths to display on the graph")

    if st.button("Calculate Option Price"):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data("AAPL")                       
            
            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, "Demo Data", 'Close')
                st.pyplot(fig)

                spot_price = current_price
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
                MC.simulate_prices()

                MC.plot_simulation_results(num_of_movements)
                st.pyplot()

                call_option_price = MC.calculate_option_price('Call Option')
                put_option_price = MC.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")

elif pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # Parameters for Binomial-Tree model
    spot_price = st.number_input(
    "Spot Price",
    min_value=1.0,
    value=100.0
    )    

    # Fetch current price
    current_price = spot_price
    
    if current_price is not None:
        st.metric("Current Spot Price", f"${current_price:.2f}")
        
        # Set default and min/max values based on current price
        default_strike = round(current_price, 2)
        min_strike = max(0.1, round(current_price * 0.5, 2))
        max_strike = round(current_price * 2, 2)
        
        strike_price = st.number_input('Strike price', 
                                       min_value=min_strike, 
                                       max_value=max_strike, 
                                       value=default_strike, 
                                       step=0.01)
        st.caption(f"The price at which the option can be exercised. Range: ${min_strike:.2f} to ${max_strike:.2f}")
    else:
        strike_price = st.number_input('Strike price', min_value=0.01, value=100.0, step=0.01)
        st.caption(
        f"The price at which the option can be exercised. Suggested range: ${min_strike:.2f} to ${max_strike:.2f}"
        )

    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    st.caption("The theoretical rate of return of an investment with zero risk. Usually based on government bonds. 0% means no risk-free return, 100% means doubling your money risk-free (unrealistic).")

    sigma = st.slider('Sigma (Volatility) (%)', 0, 100, 20)
    st.caption("A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic), 100% means extremely volatile.")

    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    st.caption("The date when the option can be exercised")

    number_of_time_steps = st.slider('Number of time steps', 5000, 100000, 15000)
    st.caption("The number of periods in the binomial tree. More steps increase accuracy but take longer to compute.")

    if st.button("Calculate Option Price"):
        try:
            with st.spinner('Fetching data...'):
                data = get_historical_data("AAPL")
            
            if data is not None and not data.empty:
                st.write("Data fetched successfully:")
                st.write(data.tail())
                
                fig = Ticker.plot_data(data, "Demo Data", 'Close')
                st.pyplot(fig)

                spot_price = current_price
                risk_free_rate = risk_free_rate / 100
                sigma = sigma / 100
                days_to_maturity = (exercise_date - datetime.now().date()).days

                BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
                call_option_price = BOPM.calculate_option_price('Call Option')
                put_option_price = BOPM.calculate_option_price('Put Option')

                st.subheader(f'Call option price: {call_option_price:.2f}')
                st.subheader(f'Put option price: {put_option_price:.2f}')
            else:
                st.error("Unable to proceed with calculations due to data fetching error.")
        except Exception as e:
            st.error(f"Error during calculation: {str(e)}")
    else:
        st.info("Click 'Calculate option price' to see results.")
elif pricing_method == OPTION_PRICING_MODEL.PAYOFF.value:

    st.header("Strategy Analytics Dashboard")

    strategy = st.selectbox(
    "Strategy",
    ["Select Strategy", "Long Call", "Long Put", "Straddle", "Strangle"]
    )

    strike_price = st.number_input(
        "Strike Price",
        min_value=1.0,
        value=100.0
    )
    upper_strike = st.number_input(
    "Upper Strike",
    min_value=1.0,
    value=110.0
    )

    stock_prices = np.arange(50, 151)
    if strategy == "Select Strategy":
        st.warning("Please select a strategy.")
        st.stop()

    if strategy == "Long Call":
        payoff = np.maximum(stock_prices - strike_price, 0)
        max_profit = "Unlimited"
        max_loss = "Premium Paid"
        break_even = strike_price

    elif strategy == "Long Put":
        payoff = np.maximum(strike_price - stock_prices, 0)
        max_profit = strike_price
        max_loss = "Premium Paid"
        break_even = strike_price

    elif strategy == "Straddle":
        call_payoff = np.maximum(stock_prices - strike_price, 0)
        put_payoff = np.maximum(strike_price - stock_prices, 0)
        payoff = call_payoff + put_payoff
        max_profit = "Unlimited"
        max_loss = "Premium Paid x 2"
        break_even = f"{strike_price} ± Premium"
    elif strategy == "Strangle":
        call_payoff = np.maximum(stock_prices - upper_strike, 0)
        put_payoff = np.maximum(strike_price - stock_prices, 0)

        payoff = call_payoff + put_payoff

        max_profit = "Unlimited"
        max_loss = "Premium Paid x 2"
        break_even = "Two Break-even Points"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Max Profit", str(max_profit))

    with col2:
        st.metric("Max Loss", str(max_loss))

    with col3:
        st.metric("Break-even", str(break_even))

    st.info(
        f"""
        Strategy Selected: {strategy}

        This graph shows the payoff at expiry for different stock prices.
        """
    )

    fig, ax = plt.subplots()

    ax.plot(stock_prices, payoff, label=strategy)

    ax.axvline(
        strike_price,
        linestyle=":",
        label=f"Strike Price ({strike_price})"
    )

    ax.axhline(0, linestyle="--")

    ax.set_xlabel("Stock Price at Expiry")
    ax.set_ylabel("Profit")
    ax.set_title(f"{strategy} Payoff Diagram")

    ax.legend()

    st.pyplot(fig)

elif pricing_method == OPTION_PRICING_MODEL.COMPARISON.value:

    st.header("Model Comparison Dashboard")

    spot_price = st.number_input(
        "Spot Price",
        min_value=1.0,
        value=100.0
    )

    strike_price = st.number_input(
        "Strike Price",
        min_value=1.0,
        value=100.0
    )

    risk_free_rate = st.slider(
        "Risk-Free Rate (%)",
        0,
        100,
        10
    )

    sigma = st.slider(
        "Volatility (%)",
        0,
        100,
        20
    )

    days_to_maturity = st.slider(
        "Days to Maturity",
        1,
        1000,
        365
    )

    if st.button("Compare Models"):
        risk_free_rate_decimal = risk_free_rate / 100
        sigma_decimal = sigma / 100

        BSM = BlackScholesModel(
            spot_price,
            strike_price,
            days_to_maturity,
            risk_free_rate_decimal,
            sigma_decimal
        )

        bs_call = BSM.calculate_option_price("Call Option")
        bs_put = BSM.calculate_option_price("Put Option")

        MC = MonteCarloPricing(
            spot_price,
            strike_price,
            days_to_maturity,
            risk_free_rate_decimal,
            sigma_decimal,
            10000
        )

        MC.simulate_prices()

        mc_call = MC.calculate_option_price("Call Option")
        mc_put = MC.calculate_option_price("Put Option")
        
        
        BOPM=BinomialTreeModel(
            spot_price,
            strike_price,
            days_to_maturity,
            risk_free_rate_decimal,
            sigma_decimal,
            100
        )

        binomial_call = BOPM.calculate_option_price("Call Option")
        binomial_put = BOPM.calculate_option_price("Put Option")

        data = {
            "Model": [
                "Black-Scholes",
                "Monte Carlo",
                "Binomial Tree"
            ],
            "Call Price": [
                round(bs_call, 2),
                round(mc_call, 2),
                round(binomial_call, 2)
            ],
            "Put Price": [
                round(bs_put, 2),
                round(mc_put, 2),
                round(binomial_put, 2)
            ]
        }
        st.success(
    "Comparison completed successfully. All models evaluated using identical market parameters."
        )
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Models Compared", "3")

        with col2:
            st.metric(
                "Highest Call Price",
                f"{max(data['Call Price']):.2f}"
            )

        with col3:
            st.metric(
                "Highest Put Price",
                f"{max(data['Put Price']):.2f}"
            )

       
       
        st.table(data)
        comparison_df = pd.DataFrame(data)

        st.subheader("Model Price Comparison")

        

        st.bar_chart(
            comparison_df.set_index("Model")[["Call Price", "Put Price"]]
        )

        
st.markdown("---")
st.caption(
    "QuantLab | Quantitative Finance & Options Analytics Platform"
)