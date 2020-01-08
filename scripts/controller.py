print("Enter the sport")
print("1. Basketball")
print("2. Football\n")
choice = input()
print("\n")
if choice.strip() == '2' or choice.lower().strip() == 'football':

    from football import fetchMatch
    fetchMatch()

elif choice.strip() == '1' or choice.lower().strip() == 'basketball':

    pass
    # from basketball import fetchMatch
    # fetchMatch()

else:
    print("Wrong input")
