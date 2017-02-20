page_dict = {}


for x in range(0, 10):
    print(x)
    page_dict[x] = {
        'title': x
    }

print(page_dict)
print(sorted(page_dict.items(), key=lambda x: x[0])[0])
