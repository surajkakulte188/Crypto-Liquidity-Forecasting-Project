# Cryptocurrency Liquidity — Exploratory Data Analysis (EDA) Report

## 1. Introduction 
- This Exploratory Data Analysis (EDA) was performed on cryptocurrency market data to understand liquidity patterns and their relation to market stability. The dataset includes historical price, trading volume, and other market factor

## 2. Dataset
- Source: CoinGecko historical cryptocurrency dataset
- Period: 2016–2017 (example dataset used for this study)
- Rows: 993 | Columns: 11 (post-clean)
- Columns: `coin, symbol, price, 1h, 24h, 7d, 24h_volume, mkt_cap, date, source_file, liquidity_ratio`
- Target proxy: `liquidity_ratio = 24h_volume / mkt_cap`
- Data Files: Daily price, trading volume, and market cap records
- Processed Files: Engineered features, lag features, and merged datasets

## 3. Data Cleaning & Preprocessing
- The following preprocessing steps were applied:
1. Handling missing values using interpolation and forward filling
2. Removing duplicate rows and ensuring timestamp consistency
3. Normalizing numerical features using MinMaxScaler
4. Creating lag features to capture short-term temporal dependencies

## 4. EDA Findings
## 4.1 Summary Statistics
- Mean daily trading volume showed high variability across periods
- Volatility (measured as standard deviation of returns) was strongly correlated with liquidity dips
- High trading volume days typically corresponded to higher liquidity levels

## 4.2 Correlation Analysis
- Trading Volume and Liquidity: Strong positive correlation
- Price Volatility and Liquidity: Negative correlation (higher volatility often reduces liquidity)
- Market Cap and Liquidity: Moderate positive correlation

## 4.3 Visual Trends
Several plots were generated to analyze trends:
- Time-series plots of trading volume, liquidity ratios, and volatility
- Heatmaps of feature correlations showing strong interaction between liquidity and market activity
- Distribution plots of returns and liquidity ratios
- Moving average plots for 7-day and 30-day liquidity trends

## 5. Feature Engineering Insights
- Based on EDA, new features were engineered:
- Rolling averages (7-day, 30-day trading volume and returns)
- Liquidity ratio: Volume / Market Cap
- Volatility index: Standard deviation of daily returns
- Lag features for volume and liquidity levels

## 6. Conclusion
- The EDA revealed that liquidity in cryptocurrency markets is heavily influenced by trading volume, market capitalization, and volatility. Periods of high volatility tend to coincide with reduced liquidity, making them critical indicators for forecasting liquidity crises. These insights guided the selection of features for the machine learning model.
