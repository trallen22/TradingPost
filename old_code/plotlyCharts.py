import plotly.graph_objects as go
import get_data

STOCK_SYMBOL = "AAPL"
START_DATE = "2024-11-04"
END_DATE = "2024-11-08"

stock_data = get_data.calculateDataBars(STOCK_SYMBOL, 1, "hour", START_DATE, END_DATE)

fig = go.Figure(data=[go.Candlestick(
                x = stock_data.index, # date values
                open = stock_data['Open'],
                high = stock_data['High'],
                low = stock_data['Low'],
                close = stock_data['Close'],
                increasing_line_color = 'green',
                decreasing_line_color = 'red')])

# Add a title
fig.update_layout(
    title="Stock Price Candlestick Chart",
    title_x=0.5,  # Center the title

    # Customize the font and size of the title
    title_font=dict(size=24, family="Arial"),

    # Set the background color of the plot
    plot_bgcolor='white',

    # Customize the grid lines
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
)

# Add a range slider and customize it
fig.update_layout(
    xaxis_rangeslider_visible=True,  # Show the range slider

    # Customize the range slider's appearance
    xaxis_rangeslider=dict(
        thickness=0.05,  # Set the thickness of the slider
        bordercolor='black',  # Set the border color
        borderwidth=1,  # Set the border width
    )
)

# Set layout size
fig.update_layout(
    autosize=False,
    width=700,  
    height=500)

# save this file as a standalong html file:
fig.write_html("test_chart.html")