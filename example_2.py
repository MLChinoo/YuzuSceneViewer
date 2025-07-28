from handlers import HandlerMeta, Handlers

if __name__ == "__main__":
    handler: HandlerMeta = Handlers["senren"]
    handler_config = handler.build_config(
        root_dir=r"C:\Users\MLChinoo\Desktop\senren_adult_scns",
        scnchartdata_filepath=r"C:\Users\MLChinoo\Desktop\senren_adult_scns\scnchartdata.tjs",
        dialogue_language_id=2
    )
    handler.clazz().handle(handler_config)
