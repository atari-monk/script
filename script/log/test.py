from log.utils import pad_two

print('Test pad_two [0,9]')
for i in range(0, 10):
    print(f"{i} -> '{pad_two(i)}'")