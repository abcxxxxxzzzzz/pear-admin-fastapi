from apps.core.config import TEMPLATES_DIR
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory=TEMPLATES_DIR)

