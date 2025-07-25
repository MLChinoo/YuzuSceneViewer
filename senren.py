import json
import os
import traceback

from py_mini_racer import MiniRacer

root_dir = r"C:\Users\MLChinoo\Desktop\senren_adult_scns"
DEBUG_SKIP = True

head_scn = "001・アーサー王ver1.07.ks"
head_label = "*com_part_1"
current_scn = head_scn

ctx = MiniRacer()
ctx.eval("""
initialize();
var flags = {
    "koh": [
        ["s507*sub_part_7_sel", 1, 1]
    ],
    "len": [
        ["s010*com_part_10_sel", 1, 1],
        ["s010*010_02A_sel", 2, 1]
    ],
    "mak": [
        ["s006*com_part_6_sel", 2, 1],
        ["s010*010_01com_sel", 2, 1]
    ],
    "mur": [
        ["s010*010_01com_sel", 3, 1],
        ["s010*010_02com_sel", 2, 1]
    ],
    "rok": [
        ["s507*sub_part_7_sel", 2, 1]
    ],
    "sub": [
        ["s001*com_part_1_sel", 1, 1],
        ["s012*com_part_12_sel", 2, 1]
    ],
    "yos": [
        ["s010*010_02A_sel", 1, 1],
        ["s014*com_part_14_sel", 1, 1]
    ]
};
function initialize() {
    this["yos"] = 0;
    this["mak"] = 0;
    this["mur"] = 0;
    this["len"] = 0;
    this["rok"] = 0;
    this["koh"] = 0;
    this["sub"] = 0;
}
function UpdateBranchFlags() {
    initialize();
    for (var character in flags) {
        var conditions = flags[character];
        for (var i = 0; i < conditions.length; i++) {
            var condition = conditions[i];
            var selection = condition[0];
            var selected_id = condition[1];
            var bonus = condition[2];
            if (this[selection] === selected_id) {
                this[character] += bonus;
            }
        }
    }
}
function SetBranchFlags(varName, value) {
    this[varName] = value;
    UpdateBranchFlags();
}
function CheckBranchFlags(expr) {
    try {
        var cleanExpr = expr.split("&&")[0].split("||")[0].trim();
        return !!eval(cleanExpr);
    } catch (e) {
        return false;
    }
}
""")

storage = head_scn
target = head_label

while current_scn:
    print()
    if current_scn == "start.ks":
        print("到达线路结尾，线路结束")
        break
    print(f"准备读取scenes：{current_scn} ...")
    with open(os.path.join(root_dir, f"{current_scn}.json"), mode="r", encoding="UTF-8") as file:
        loaded_json = json.load(file)
        print(f"读取scenes：{current_scn} 成功")
        print(f"name: {loaded_json["name"]}")
        input("[DEBUG]回车继续")
        assert storage == loaded_json["name"]
        print("————————————————————")
        scenes_map = {}
        min_first_line = 2147483647
        for scene_cached in loaded_json["scenes"]:
            scenes_map[scene_cached["label"]] = scene_cached
            min_first_line = current_first_line if (current_first_line := int(scene_cached["firstLine"])) < min_first_line else min_first_line
        if target is None:
            for scene in scenes_map.values():
                if scene["firstLine"] == min_first_line:
                    target = scene["label"]
        while True:
            scene = scenes_map[target]
            print("当前scene：")
            print(f"firstLine: {scene["firstLine"]}")
            print(f"label: {scene["label"]}（应与上一个target一致）")
            print(f"title: {scene["title"]}")
            print()
            print(f"芳乃: {ctx.eval("yos")}")
            print(f"茉子: {ctx.eval("mak")}")
            print(f"丛雨: {ctx.eval("mur")}")
            print(f"蕾娜: {ctx.eval("len")}")
            print(f"芦花: {ctx.eval("rok")}")
            print(f"小春: {ctx.eval("koh")}")
            print(f"芦花小春共用线: {ctx.eval("sub")}")
            print()
            assert scene["label"] == target
            # assert ("selects" in scene.keys()) ^ ("nexts" in scene.keys())  # 假定texts和selects不会同时存在，texts存在时nexts也一定存在

            if "selects" in scene.keys():  # 当前scene含有选择块
                print(f"模式：select")
                selects_map = {}
                for select_cached in scene["selects"]:
                    selects_map[int(select_cached["selidx"])] = select_cached
                valid_indexes = list(selects_map.keys())
                valid_indexes.sort()
                valid_indexes = tuple(str(_) for _ in valid_indexes)
                for index in valid_indexes:
                    select = selects_map[index := int(index)]
                    print(f"({index}) 第{index}个选项：")
                    print(f"\t[日文]{select["text"]}")
                    for index_lang, lang in enumerate(("英文", "简中", "繁中"), start=1):
                        print(f"\t[{lang}]{select["language"][index_lang]["text"]}")
                    print(f"\ttag: {select["tag"]}")
                    print(f"\texp: {select["exp"]}")
                    print(f"\tstorage: {select["storage"]}")
                    print(f"\ttarget: {select["target"]}")
                selected_id = ""
                while selected_id not in valid_indexes :
                    selected_id = input("输入选项序号，按回车键确定：")
                selected = scene["selects"][int(selected_id)]
                try:
                    rtn = ctx.eval(selected["exp"])
                    print(f"执行exp成功，返回值：{rtn}")
                except Exception:
                    print(f"执行exp失败，异常：")
                    traceback.print_exc()
                    print("可能影响后续路线走向！！")
                finally:
                    print()
                    storage = selected["storage"]
                    target = selected["target"]

            elif "nexts" in scene.keys():  # 当前scene含有文本块  # 除选择scene外，nexts一定存在，否则原游戏的场景无法继续
                if "texts" in scene.keys():
                    print(f"模式：text")
                    for text in scene["texts"]:
                        speaker_name = text[0]
                        # _ = text[1]
                        dialogue_multi_lang = text[2]
                        print()
                        print(f"原始说话人：{speaker_name}")
                        for index, lang in enumerate(("日文", "英文", "简中", "繁中")):
                            speaker_alias = dialogue_multi_lang[index][0]
                            dialogue_text = dialogue_multi_lang[index][1]
                            print(f"[{lang}]{speaker_alias}: {dialogue_text}")
                        if not DEBUG_SKIP:
                            input("按回车键继续：")
                else:
                    print(f"模式：next")

                nexts_map = {}
                for next_cached in scene["nexts"]:
                    signature = f"{next_cached.get("eval")}|{next_cached.get("storage")}|{next_cached.get("target")}|{next_cached.get("type")}"
                    nexts_map[signature] = next_cached
                nexts_eval = []
                nexts_non_eval = []
                for next_cached in nexts_map.values():
                    if "eval" in next_cached.keys():
                        nexts_eval.append(next_cached)
                    else:
                        nexts_non_eval.append(next_cached)
                assert len(nexts_non_eval) == 1
                for next_eval in nexts_eval:
                    if ctx.eval(next_eval["eval"]):
                        storage = next_eval["storage"]
                        target = next_eval["target"]
                        break
                else:
                    storage = nexts_non_eval[0]["storage"]
                    if "target" in nexts_non_eval[0].keys():
                        target = nexts_non_eval[0]["target"]
                    else:
                        target = None

            else:
                raise RuntimeError("?")

            assert storage is not None
            print()
            print("下一个scene：")
            print(f"storage: {storage}")
            print(f"target: {target}")
            print("————————————————————")
            if storage != current_scn:
                print("storage发生变化，准备读取下一个scenes...")
                current_scn = storage
                break
