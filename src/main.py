import sys
import os

# Agrega el directorio src al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/martinjauma/Documents/CODIGO/TEROS/gesdepo/src/')))

from forms.form import main  # Asegúrate de que 'main' es la función o clase que ejecuta la lógica de Streamlit

if __name__ == "__main__":
    main()
