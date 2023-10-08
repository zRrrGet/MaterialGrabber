from src.core.external.components.content_downloader.sources.base.toolxox import ToolxoxClient


class VideezyClient(ToolxoxClient):

    @property
    def endpoint(self) -> str:
        return 'https://toolxox.com/dl/2/vidzy/get.php'
