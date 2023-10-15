from dataclasses import dataclass

from src.core.domain.entities.download_request import ContentType


def content_type_to_str(content_type: ContentType) -> str:
    return {
        ContentType.photo: 'Фото',
        ContentType.video: 'Видео'
    }[content_type]


@dataclass
class ContentStock:
    title: str
    supported_content_types: list[ContentType]

    @property
    def content_type_titles(self) -> list[list]:
        return list(map(lambda c_type: [content_type_to_str(c_type), c_type.value], self.supported_content_types))

    @property
    def html_link(self) -> str:
        return f'<a href="{self.title}">{self.title}</a>'


def get_content_stocks() -> list[ContentStock]:
    return [
        ContentStock('depositphotos.com', [ContentType.photo, ContentType.video]),
        ContentStock('elements.envato.com', [ContentType.photo]),
        ContentStock('istockphoto.com', [ContentType.photo, ContentType.video]),
        ContentStock('eyeem.com', [ContentType.photo]),
        ContentStock('gettyimages.com', [ContentType.photo, ContentType.video]),
        ContentStock('motionarray.com', [ContentType.photo]),
        ContentStock('shutterstock.com', [ContentType.photo]),
        ContentStock('storyblocks.com', [ContentType.photo, ContentType.video]),
        ContentStock('videezy.com', [ContentType.video]),
        ContentStock('agefotostock.com', [ContentType.photo]),
    ]


def get_content_stock(stock_title: str) -> ContentStock:
    return next(filter(lambda stock: stock.title == stock_title, get_content_stocks()))


def get_stock_titles() -> list[list[str]]:
    return list(map(lambda stock: [stock.title], get_content_stocks()))
