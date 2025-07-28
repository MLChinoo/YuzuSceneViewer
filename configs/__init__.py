from abc import abstractmethod
from typing import final, Any

from pydantic import BaseModel, Field


class BaseConfig(BaseModel):
    # 所有Handler共用配置
    root_dir: str = Field(..., description="存放所有dump后的场景json的目录路径")

    scnchartdata_filepath: str = Field(..., description="scnchartdata.tjs文件路径，用于分支跳转")

    skip_texts: bool = Field(True, description="跳过显示剧情对话时的“按回车键继续”，不跳过可在终端内交互式浏览剧情")

    # 日文：0  英文：1  简中：2  繁中：3
    dialogue_language_id: int = Field(2, description="写文件时对话文本的语言序号")

    output_txt_filepath: str = Field("output.txt", description="输出txt文件路径")

    output_pdf_filepath: str = Field("output.pdf", description="输出pdf文件路径")

    def __init__(self, root_dir: str, scnchartdata_filepath: str, **data: Any):
        data["root_dir"] = root_dir
        data["scnchartdata_filepath"] = scnchartdata_filepath
        super().__init__(**data)

    @final
    def check_valid(self):
        self._check_valid()

    @abstractmethod
    def _check_valid(self):
        pass
