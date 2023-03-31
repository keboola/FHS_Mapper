import streamlit as st

st.title('Firehouse Subs Mapper')


# replace by classes
classes = ['Paris', 'Prague', 'Berlin', 'Rome']

# replace by locations
locations = ['Italy', 'Czechia', 'Germany', 'France']

#classes_col, locations_col = st.columns(2)
#row = st.columns(1)

for i in range(len(classes)):
#    with row:
    classes_col, locations_col = st.columns(2)
    with classes_col:
        ##st.text(classes[i])
        st.markdown(f" ### {classes[i]} &#8594;")
    with locations_col:
        st.selectbox("select mapping", locations, key=f"class_{i}")


import pandas as pd

df = pd.DataFrame(
    {"select mapping": locations}
)
df["select mapping"] = (
    df["select mapping"].astype("category"))

s = df.style

cell_color = pd.DataFrame([True, True, True, True],
                          index=df.index,
                          columns=df.columns)
s.set_td_classes(cell_color)

df["select mapping"].style.
df.index=classes

edited_df = st.experimental_data_editor(df, width=1000)


df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

edited_df = st.experimental_data_editor(df) # 👈 An editable dataframe



favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")