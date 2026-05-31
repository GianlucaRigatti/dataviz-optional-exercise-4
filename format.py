def format_population(value: float) -> str:
	if value >= 1_000_000_000:
		return f"{value / 1_000_000_000:.2f}B"
	if value >= 1_000_000:
		return f"{value / 1_000_000:.1f}M"
	return f"{value:,.0f}"


def format_currency(value: float) -> str:
	return f"${value:,.2f}"


def format_year(value: float) -> str:
    return f"{value:.1f} year{'s' if abs(value) != 1 else ''}"