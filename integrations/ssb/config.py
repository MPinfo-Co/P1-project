from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SSB 連線
    SSB_HOST: str = "https://192.168.10.48"
    SSB_LOGSPACE: str = "ALL"
    SSB_USERNAME: str = ""
    SSB_PASSWORD: str = ""

    SSB_SEARCH_EXPRESSION: str = (
        # Windows AD 資安事件
        "nvpair:.sdata.win@18372.4.event_id=4625 OR "  # 登入失敗
        "nvpair:.sdata.win@18372.4.event_id=4648 OR "  # 明確憑證登入（RunAs）
        "nvpair:.sdata.win@18372.4.event_id=4720 OR "  # 新建帳號
        "nvpair:.sdata.win@18372.4.event_id=4722 OR "  # 啟用帳號
        "nvpair:.sdata.win@18372.4.event_id=4725 OR "  # 停用帳號
        "nvpair:.sdata.win@18372.4.event_id=4740 OR "  # 帳號鎖定
        "nvpair:.sdata.win@18372.4.event_id=4719 OR "  # 稽核政策變更
        "nvpair:.sdata.win@18372.4.event_id=4726 OR "  # 刪除帳號
        "nvpair:.sdata.win@18372.4.event_id=4728 OR "  # 加入全域安全群組
        "nvpair:.sdata.win@18372.4.event_id=4732 OR "  # 加入本機安全群組
        "nvpair:.sdata.win@18372.4.event_id=4756 OR "  # 加入萬用安全群組
        "nvpair:.sdata.win@18372.4.event_id=1102 OR "  # 安全日誌被清除
        # FortiGate 防火牆
        "nvpair:.sdata.forti.action=deny OR "  # 拒絕連線
        "nvpair:.sdata.forti.level=warning"    # 警告等級
    )

    SSB_SEARCH_EXPRESSION_WINDOWS_ONLY: str = (
        "nvpair:.sdata.win@18372.4.event_id=4625 OR "
        "nvpair:.sdata.win@18372.4.event_id=4648 OR "
        "nvpair:.sdata.win@18372.4.event_id=4720 OR "
        "nvpair:.sdata.win@18372.4.event_id=4722 OR "
        "nvpair:.sdata.win@18372.4.event_id=4725 OR "
        "nvpair:.sdata.win@18372.4.event_id=4740 OR "
        "nvpair:.sdata.win@18372.4.event_id=4719 OR "
        "nvpair:.sdata.win@18372.4.event_id=4726 OR "
        "nvpair:.sdata.win@18372.4.event_id=4728 OR "
        "nvpair:.sdata.win@18372.4.event_id=4732 OR "
        "nvpair:.sdata.win@18372.4.event_id=4756 OR "
        "nvpair:.sdata.win@18372.4.event_id=1102"
    )

    # 分析模式
    ANALYSIS_MODE: str = "full"  # "full" | "windows_only"

    # P1-code ingest endpoint
    P1_CODE_URL: str = "http://localhost:8000"

    # 帳密（需在 .env 設定）
    INGEST_SECRET: str = ""

    @property
    def effective_search_expression(self) -> str:
        if self.ANALYSIS_MODE == "windows_only":
            return self.SSB_SEARCH_EXPRESSION_WINDOWS_ONLY
        return self.SSB_SEARCH_EXPRESSION

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
