from handlers import Handlers, HandlerMeta

if __name__ == "__main__":
    print("\n选择游戏：")
    handler_names = list(Handlers.keys())

    for index, name in enumerate(handler_names):
        desc = Handlers[name].description
        print(f"\t【{index}】{name} - {desc}")

    selected_id = None
    while selected_id not in (str(i) for i in range(len(handler_names))):
        selected_id = input("请输入编号：")

    selected_name = handler_names[int(selected_id)]

    handler: HandlerMeta = Handlers[selected_name]
    handler_config = handler.build_config(
        root_dir=r"C:\Users\MLChinoo\Desktop\tenshi_dumps\allscns",
        scnchartdata_filepath=r"C:\Users\MLChinoo\Desktop\tenshi_dumps\Extractor_Output\adult\4C9461238F67DF8F1766B263B78F44AD4F6A6E8BCBA9B7CD6A05874FEF209223.txt"
    )
    handler.clazz().handle(handler_config)

