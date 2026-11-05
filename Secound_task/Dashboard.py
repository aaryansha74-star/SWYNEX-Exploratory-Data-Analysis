
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# 1. LOAD CUSTOMER DATAA

FILE_NAME = "Cleaned_Customer_Dataset.xlsx"

try:
    df = pd.read_excel(
        FILE_NAME,
        sheet_name="Cleaned_Data"
    )

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Purchase_Amount_NPR"] = pd.to_numeric(
        df["Purchase_Amount_NPR"], errors="coerce"
    )
    df["Signup_Date"] = pd.to_datetime(
        df["Signup_Date"], errors="coerce"
    )

except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Dataset Error",
        f"Could not load the Excel file.\n\n{e}\n\n"
        "Make sure the Excel file is in the same folder "
        "as customer_eda.py."
    )
    root.destroy()
    raise SystemExit


# 2. MAIN WINDOW


root = tk.Tk()

root.title("Customer Analytics Dashboard")
root.geometry("1250x850")
root.minsize(900, 650)

BACKGROUND = "#D6D9FC"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#243447"

root.configure(bg=BACKGROUND)

sns.set_theme(style="whitegrid")
# 3. SCROLLABLE DASHBOARD
main_canvas = tk.Canvas(
    root,
    bg=BACKGROUND,
    highlightthickness=0
)

vertical_scroll = ttk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

main_canvas.configure(
    yscrollcommand=vertical_scroll.set
)

vertical_scroll.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

dashboard = tk.Frame(
    main_canvas,
    bg=BACKGROUND
)

window_id = main_canvas.create_window(
    (0, 0),
    window=dashboard,
    anchor="nw"
)


def update_scroll_region(event=None):
    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


def update_dashboard_width(event):
    main_canvas.itemconfigure(
        window_id,
        width=event.width
    )


dashboard.bind("<Configure>", update_scroll_region)
main_canvas.bind("<Configure>", update_dashboard_width)


# Mouse wheel scrolling
def mouse_wheel(event):
    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
main_canvas.bind_all("<MouseWheel>", mouse_wheel)
# 4. HEADER
header = tk.Frame(
    dashboard,
    bg="#172B4D",
    height=120
)

header.pack(fill="x", padx=15, pady=15)
header.pack_propagate(False)

tk.Label(
    header,
    text="CUSTOMER ANALYTICS DASHBOARD",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#172B4D"
).pack(pady=(25, 5))

tk.Label(
    header,
    text="Exploratory Data Analysis | Customer Behaviour | Purchase Insights",
    font=("Arial", 11),
    fg="#DCE6F1",
    bg="#172B4D"
).pack()


# 5. KPI CARDS


total_customers = len(df)

total_purchase = df["Purchase_Amount_NPR"].sum()

average_purchase = df["Purchase_Amount_NPR"].mean()

average_age = df["Age"].mean()

kpi_frame = tk.Frame(
    dashboard,
    bg=BACKGROUND
)

kpi_frame.pack(fill="x", padx=15, pady=5)

kpis = [
    ("TOTAL CUSTOMERS", f"{total_customers:,}"),
    ("TOTAL PURCHASE", f"NPR {total_purchase:,.0f}"),
    (
        "AVERAGE PURCHASE",
        f"NPR {average_purchase:,.0f}"
        if pd.notna(average_purchase) else "N/A"
    ),
    (
        "AVERAGE AGE",
        f"{average_age:.1f} years"
        if pd.notna(average_age) else "N/A"
    )
]

for i, (label, value) in enumerate(kpis):

    card = tk.Frame(
        kpi_frame,
        bg=CARD_COLOR,
        highlightbackground="#D9E2EF",
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=i,
        padx=6,
        pady=8,
        sticky="nsew"
    )

    tk.Label(
        card,
        text=label,
        font=("Arial", 10, "bold"),
        bg=CARD_COLOR,
        fg="#64748B"
    ).pack(pady=(15, 5))

    tk.Label(
        card,
        text=value,
        font=("Arial", 17, "bold"),
        bg=CARD_COLOR,
        fg="#2457A7"
    ).pack(pady=(5, 15))

    kpi_frame.columnconfigure(i, weight=1)



# 6. SECTION HEADING


def add_heading(title):

    tk.Label(
        dashboard,
        text=title,
        font=("Arial", 17, "bold"),
        bg=BACKGROUND,
        fg=TEXT_COLOR,
        anchor="w"
    ).pack(fill="x", padx=20, pady=(20, 5))



# 7. MATPLOTLIB CHART AREA


add_heading("Customer Demographics & Purchase Analysis")

chart_frame = tk.Frame(
    dashboard,
    bg=CARD_COLOR,
    highlightbackground="#9AC3FD",
    highlightthickness=1
)

chart_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

fig = Figure(
    figsize=(14, 29),
    dpi=90,
    facecolor="white"
)

axes = fig.subplots(5, 2)

fig.subplots_adjust(
    hspace=0.55,
    wspace=0.35,
    top=0.97,
    bottom=0.03
)



# CHART 1: AGE DISTRIBUTION


age_data = df["Age"].dropna()

if not age_data.empty:

    sns.histplot(
        age_data,
        bins=12,
        kde=True,
        ax=axes[0, 0],
        color="#4472C4"
    )

axes[0, 0].set_title(
    "Age Distribution",
    fontweight="bold"
)

axes[0, 0].set_xlabel("Age")
axes[0, 0].set_ylabel("Customers")



# CHART 2: GENDER DISTRIBUTION


gender_data = df["Gender"].dropna().value_counts()

if not gender_data.empty:

    axes[0, 1].pie(
        gender_data.values,
        labels=gender_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

axes[0, 1].set_title(
    "Gender Distribution",
    fontweight="bold"
)



# CHART 3: PURCHASE BY CATEGORY


category_data = (
    df.groupby("Category")["Purchase_Amount_NPR"]
    .sum()
    .sort_values(ascending=False)
    .dropna()
)

if not category_data.empty:

    category_data.plot(
        kind="bar",
        ax=axes[1, 0],
        color="#4472C4"
    )

axes[1, 0].set_title(
    "Purchase by Category",
    fontweight="bold"
)

axes[1, 0].set_ylabel("Purchase Amount (NPR)")
axes[1, 0].tick_params(axis="x", rotation=30)



# CHART 4: PURCHASE CHANNEL

channel_data = (
    df.groupby("Purchase_Channel")["Purchase_Amount_NPR"]
    .sum()
    .dropna()
)

if not channel_data.empty:

    axes[1, 1].pie(
        channel_data.values,
        labels=channel_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

axes[1, 1].set_title(
    "Purchase by Channel",
    fontweight="bold"
)



# CHART 5: MONTHLY SIGNUPS


signup_data = df.dropna(
    subset=["Signup_Date"]
).copy()

if not signup_data.empty:

    signup_data["Month"] = (
        signup_data["Signup_Date"].dt.to_period("M")
    )

    monthly_data = (
        signup_data.groupby("Month")
        .size()
    )

    axes[2, 0].plot(
        monthly_data.index.astype(str),
        monthly_data.values,
        marker="o",
        linewidth=2,
        color="#2E86AB"
    )

    axes[2, 0].tick_params(
        axis="x",
        rotation=45
    )

axes[2, 0].set_title(
    "Monthly Customer Signups",
    fontweight="bold"
)

axes[2, 0].set_ylabel("Number of Signups")



# CHART 6: TOP CITIES


city_data = (
    df.groupby("City")["Purchase_Amount_NPR"]
    .sum()
    .sort_values(ascending=False)
    .dropna()
    .head(10)
)

if not city_data.empty:

    city_data.sort_values().plot(
        kind="barh",
        ax=axes[2, 1],
        color="#70AD47"
    )

axes[2, 1].set_title(
    "Top 10 Cities by Purchase",
    fontweight="bold"
)

axes[2, 1].set_xlabel("Purchase Amount (NPR)")



# CHART 7: AGE GROUP ANALYSIS


age_groups = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

age_group_data = age_groups.value_counts().sort_index()

age_group_data.plot(
    kind="bar",
    ax=axes[3, 0],
    color="#ED7D31"
)

axes[3, 0].set_title(
    "Customers by Age Group",
    fontweight="bold"
)

axes[3, 0].set_ylabel("Customers")
axes[3, 0].tick_params(axis="x", rotation=0)


#
# CHART 8: PURCHASE DISTRIBUTION


purchase_data = df["Purchase_Amount_NPR"].dropna()

if not purchase_data.empty:

    sns.histplot(
        purchase_data,
        bins=12,
        kde=True,
        ax=axes[3, 1],
        color="#E69F00"
    )

axes[3, 1].set_title(
    "Purchase Amount Distribution",
    fontweight="bold"
)

axes[3, 1].set_xlabel("Purchase Amount (NPR)")



# CHART 9: MISSING VALUES


missing_data = (
    df.isnull()
    .sum()
)

missing_data = missing_data[
    missing_data > 0
].sort_values()

if not missing_data.empty:

    missing_data.sort_values().plot(
        kind="barh",
        ax=axes[4, 0],
        color="#C0504D"
    )

axes[4, 0].set_title(
    "Missing Values by Column",
    fontweight="bold"
)

axes[4, 0].set_xlabel("Missing Count")



# CHART 10: OUTLIER ANALYSIS


if not purchase_data.empty:

    sns.boxplot(
        y=purchase_data,
        ax=axes[4, 1],
        color="#70AD47"
    )

axes[4, 1].set_title(
    "Purchase Amount Outlier Detection",
    fontweight="bold"
)

axes[4, 1].set_ylabel("Purchase Amount (NPR)")



# DISPLAY CHARTS IN TKINTER


fig.tight_layout(pad=3)

chart_canvas = FigureCanvasTkAgg(
    fig,
    master=chart_frame
)

chart_canvas.draw()

chart_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# ==========================================
# 8. AGE VS PURCHASE ANALYSIS
# ==========================================

add_heading("Customer Behaviour Analysis")

scatter_frame = tk.Frame(
    dashboard,
    bg=CARD_COLOR,
    highlightbackground="#D9E2EF",
    highlightthickness=1
)

scatter_frame.pack(
    fill="both",
    padx=15,
    pady=10
)

scatter_fig = Figure(
    figsize=(12, 4),
    dpi=90,
    facecolor="white"
)

scatter_ax = scatter_fig.add_subplot(111)

scatter_data = df.dropna(
    subset=["Age", "Purchase_Amount_NPR"]
)

if not scatter_data.empty:

    sns.scatterplot(
        data=scatter_data,
        x="Age",
        y="Purchase_Amount_NPR",
        hue="Category",
        ax=scatter_ax
    )

scatter_ax.set_title(
    "Age vs Purchase Amount",
    fontweight="bold"
)

scatter_fig.tight_layout()

scatter_canvas = FigureCanvasTkAgg(
    scatter_fig,
    master=scatter_frame
)

scatter_canvas.draw()

scatter_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# 9. OUTLIER SUMMARY
if not purchase_data.empty:

    Q1 = purchase_data.quantile(0.25)
    Q3 = purchase_data.quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = purchase_data[
        (purchase_data < lower_limit) |
        (purchase_data > upper_limit)
    ]

else:
    outliers = pd.Series(dtype=float)



# 10. DATA QUALITY SUMMARY

add_heading("Data Quality Summary")

quality_frame = tk.Frame(
    dashboard,
    bg=CARD_COLOR,
    highlightbackground="#D9E2EF",
    highlightthickness=1
)

quality_frame.pack(
    fill="x",
    padx=15,
    pady=10
)

quality_text = (
    f"Total Records: {len(df)}\n"
    f"Total Columns: {len(df.columns)}\n"
    f"Missing Values: {df.isnull().sum().sum()}\n"
    f"Purchase Outliers: {len(outliers)}\n"
    f"Valid Purchase Records: {purchase_data.count()}\n"
    f"Valid Age Records: {age_data.count()}"
)

tk.Label(
    quality_frame,
    text=quality_text,
    font=("Arial", 12),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    justify="left",
    anchor="w"
).pack(
    padx=20,
    pady=15,
    fill="x"
)

# 11. CUSTOMER DATA TABLE


add_heading("Complete Customer Dataset")

table_frame = tk.Frame(
    dashboard,
    bg=CARD_COLOR
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

table = ttk.Treeview(
    table_frame,
    columns=list(df.columns),
    show="headings",
    height=12
)

vertical_table_scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

horizontal_table_scroll = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=table.xview
)

table.configure(
    yscrollcommand=vertical_table_scroll.set,
    xscrollcommand=horizontal_table_scroll.set
)

vertical_table_scroll.pack(
    side="right",
    fill="y"
)

horizontal_table_scroll.pack(
    side="bottom",
    fill="x"
)

table.pack(
    side="left",
    fill="both",
    expand=True
)

for column in df.columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=140,
        minwidth=100
    )

for _, row in df.iterrows():

    values = [
        "" if pd.isna(value) else str(value)
        for value in row
    ]

    table.insert(
        "",
        "end",
        values=values
    )



# 12. FOOTER


footer = tk.Frame(
    dashboard,
    bg="#172B4D",
    height=65
)

footer.pack(
    fill="x",
    padx=15,
    pady=(20, 15)
)

tk.Label(
    footer,
    text="CUSTOMER DATA ANALYTICS",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#172B4D"
).pack(pady=20)
# 13. START APPLICATION
root.mainloop()
