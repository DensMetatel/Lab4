import pandas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot


CSV_PATH = "youtube_data.csv"
df = pandas.read_csv(CSV_PATH)

df["Views"] = (df["Views"].astype(str).str.replace(",", "", regex=False).astype(int))
df["Artist"] = df["Video"].str.split("-").str[0].str.strip()
df = df.dropna(subset=["Artist", "Views"])

top_10_artists = df["Artist"].value_counts().head(10)

top_artists_list = top_10_artists.index.tolist()

top_group = df[df["Artist"].isin(top_artists_list)]["Views"]
other_group = df[~df["Artist"].isin(top_artists_list)]["Views"]

mean_top = top_group.mean()
mean_other = other_group.mean()

print("\nСреднее количество просмотров:")
print(f"Топ-исполнители: {mean_top:,.0f}")
print(f"Остальные: {mean_other:,.0f}")

if mean_top > mean_other:
    print("\nГипотеза подтверждена: топ-исполнители популярнее")
else:
    print("\nГипотеза не подтверждена")

matplotlib.pyplot.figure(figsize=(10, 6))
matplotlib.pyplot.barh(top_10_artists.index, top_10_artists.values)
matplotlib.pyplot.xlabel("Количество появлений в топе")
matplotlib.pyplot.title("Топ-10 самых популярных исполнителей на YouTube")
matplotlib.pyplot.gca().invert_yaxis()
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig("top_artists.png")
matplotlib.pyplot.close()


matplotlib.pyplot.figure(figsize=(8, 5))
matplotlib.pyplot.bar(["Топ-исполнители", "Остальные"], [mean_top, mean_other])
matplotlib.pyplot.ylabel("Среднее количество просмотров")
matplotlib.pyplot.title("Сравнение популярности песен")
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig("comparison.png")
matplotlib.pyplot.close()
