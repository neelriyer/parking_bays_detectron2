dict = {'hello':'world'}

print(dict)

with open("Output.txt", "w") as text_file:
	print("dict['hello'] {}".format(dict['hello']), file=text_file)
