# this is where we can implement the black-sholes model for options
# 
# C = N(d_1)S_t - N(d_2)Ke^(-rt)
# where
# d_1 = (ln(S_t/K) + (r + (@^2)/2)t) / (@-/2) 
# d_2 = d_1 - @-/t
# 
# 
# C	=	call option price
# N	=	CDF of the normal distribution
# S_t	=	spot price of an asset
# K	=	strike price
# r	=	risk-free interest rate
# t	=	time to maturity
# @	=	volatility of the asset

