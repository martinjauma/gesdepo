import streamlit as st

def main():
    st.title("Teros")

    # Agregar video usando st.video() con estilo CSS para ajustar tamaño
    
    col1, col2, col3, col4,col5 = st.columns([1,1,2,1,1])
    
    with col3:
        st.video("app/assets/Teos.mp4")
   
if __name__ == "__main__":
    main()
