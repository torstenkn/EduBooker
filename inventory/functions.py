def validate_isbn13(isbn):
	"""
	Validate the ISBN-13 checksum.
	
	:param isbn: The ISBN-13 number as a string or integer.
	:return: True if valid, False if not.
	"""
	# Try to convert to string if the input is not already a string
	if not isinstance(isbn, str):
		try:
			isbn = str(isbn)
		except ValueError:
			return False
		
	# Ensure the ISBN is exactly 13 characters long and contains only digits
	if len(isbn) != 13 or not isbn.isdigit():
		return False
	
	# Convert ISBN into a list of integers
	digits = list(map(int, isbn))
	
	# Calculate the check digit using the first 12 digits
	total = 0
	for i in range(12):
		if i % 2 == 0:
			total += digits[i] * 1
		else:
			total += digits[i] * 3
			
	remainder = total % 10
	check_digit = 0 if remainder == 0 else 10 - remainder
	
	# Compare with the actual check digit (13th digit)
	return check_digit == digits[12]
