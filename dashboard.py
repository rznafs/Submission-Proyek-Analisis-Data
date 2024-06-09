import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import streamlit as st


# Membaca semua data yang dibutuhkan
all_data = pd.read_csv("Data/all_data.csv")


# Membuat sidebar
with st.sidebar:
    payment_type = st.multiselect(
        "Select Payment Type:",
        options = all_data['payment_type'].unique(),
        default = all_data['payment_type'].unique()
    )
    rating = st.multiselect(
        "Select Number of Rating:",
        options = all_data['review_score'].unique()
    )

all_data_df = all_data.query("(payment_type == @payment_type)")


# Halaman Utama
st.title('E-commerce Analysis Dashboard')
st.markdown("#")


# Visualisasi produk yang paling sering dan paling jarang dibeli
st.header("Most & Least Purchased Product")

fig_product, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 10))

colors1 = ["#95E588", "#95E588", "#95E588", "#95E588", "#95E588"]
colors2 = ["#E58888", "#E58888", "#E58888", "#E58888", "#E58888"]

sum_order_items = all_data.groupby("product_category_name_english").product_id.count().sort_values(ascending=False).reset_index()
sum_order_items.rename(columns={"product_id": "products"},inplace=True)
sum_order_items.head()

sn.barplot(
    x = "products",
    y = "product_category_name_english",
    data = sum_order_items.head(5),
    palette = colors1,
    ax = ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most frequently purchased products", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sn.barplot(
    x = "products",
    y = "product_category_name_english", 
    data = sum_order_items.sort_values(by="products", ascending=True).head(5),
    palette = colors2,
    ax = ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Most rarely purchased products", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig_product)



# Visualisasi metode Pembayaran yang banyak digunakan
st.header("Most Used Payment Type")

payment_type_counts = all_data_df.groupby(by="payment_type").customer_id.nunique().sort_values(ascending=False).reset_index()
payment_type_counts.rename(columns={"customer_id": "customers"}, inplace=True)
payment_type_counts.head()

fig_payment = plt.figure(figsize=(10, 5))

colors = ["#95E588", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"] 
sn.barplot(
    y = "customers", 
    x = "payment_type",
    data = payment_type_counts.sort_values(by="customers", ascending=False),
    palette = colors
)
plt.ylabel(None)
plt.xlabel("Payment Type")
plt.tick_params(axis='x', labelsize=12)

st.pyplot(fig_payment)


# Visualisasi tingkat kepuasan pelanggan
st.header("Customers Rating")

review_scores = all_data.groupby(by="review_score").order_id.count().reset_index()
review_scores.rename(columns={"order_id": "review_counts"}, inplace=True)
review_scores.head()

fig_rating = plt.figure(figsize=(10, 5))

colors=[]
 
sn.barplot(
    y = "review_counts", 
    x = "review_score",
    data = review_scores,
    palette = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#95E588"]
)
plt.ylabel(None)
plt.xlabel("Rating")
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig_rating)

# Menampilkan rata-rata rating
average_rating = round(all_data['review_score'].mean(), 1)
review_counts = round(all_data['review_score'].count())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Total Rating:")
    st.subheader(f"{review_counts}")
with col2:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} :star:")
