from todo import ToDoList

todo = ToDoList()

while True:
    print("\n🔹 منوی برنامه:")
    print("1. نمایش کارها")
    print("2. افزودن کار جدید")
    print("3. حذف کار")
    print("4. خروج")

    choice = input("انتخاب شما: ").strip()

    if choice == "1":
        todo.show_tasks()
    elif choice == "2":
        title = input("عنوان کار جدید: ").strip()
        if title:
            todo.add_task(title)
        else:
            print("❗ عنوان نباید خالی باشد.")
    elif choice == "3":
        todo.show_tasks()
        try:
            index = int(input("شماره کاری که می‌خواهید حذف کنید: ")) - 1
            todo.remove_task(index)
        except ValueError:
            print("❗ لطفاً یک عدد وارد کنید.")
    elif choice == "4":
        print("خروج از برنامه. 🖐️")
        break
    else:
        print("❗ گزینه معتبر نیست.")