import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr

def analyze_attendance(file):
    # Load CSV file
    df = pd.read_csv(file)
    df.set_index("Student", inplace=True)
    # Calculate total present/absent and attendance percentage
    df["Total_Present"] = df.sum(axis=1)
    df["Total_Absent"] = (df == 0).sum(axis=1)
    total_days = df.shape[1] - 2
    day_wise_attendance = df.iloc[:, :total_days].sum()

    presentage = (df["Total_Present"] / total_days) * 100
    df["Attendance_Percentage"] = presentage

    chronic_absentees = df[df["Attendance_Percentage"] < 60]
    regular_absentees = df[df["Attendance_Percentage"] >= 75]

    # Daily heatmap (save to file for Gradio Image output)
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        df.iloc[:, :total_days],
        cmap="YlGnBu",
        cbar_kws={"label": "Attendance (1 = Present, 0 = Absent)"}
    )
    plt.title("Student Attendance Heatmap (One Academic Year)")
    plt.xlabel("Days")
    plt.ylabel("Students")
    plt.tight_layout()
    daily_heatmap_path = "daily_heatmap.png"
    plt.savefig(daily_heatmap_path)
    plt.close()

    # Distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Attendance_Percentage"], bins=10, kde=True)
    plt.title("Distribution of Attendance Percentage")
    plt.xlabel("Attendance Percentage")
    plt.ylabel("Number of Students")
    distribution_path = "attendance_distribution.png"
    plt.savefig(distribution_path)
    plt.close()
    
    # monthly attendance calculation
    month_days = {
        "Jan": (0, 20),
        "Feb": (20, 40),
        "Mar": (40, 60),
        "Apr": (60, 80),
        "May": (80, 100),
        "Jun": (100, 120),
        "Jul": (120, 140),
        "Aug": (140, 160),
        "Sep": (160, 180),
        "Oct": (180, 200),
        "nov": (200, 220),
        "Dec": (220, 240),
    }
    
    monthly_df = pd.DataFrame(index=df.index)
    for month, (start, end) in month_days.items():
        monthly_df[month] = df.iloc[:, start:end].sum(axis=1)
    
    print("\nMonthly Attendance Data (Preview):\n")
    print(monthly_df)
    print("done")
    monthly_df.to_csv('monthly_attendance.csv' )
    
    # montly attendance visualization
    plt.figure(figsize=(12, 6))     
    monthly_df.mean().plot(kind='bar', color='skyblue')
    plt.title("Average Monthly Attendance") 
    plt.xlabel("Month")
    plt.ylabel("Average Days Present")
    monthly_bar_path = "monthly_attendance.png"
    plt.savefig(monthly_bar_path)
    plt.close()
    
    # monthly heatmap
    plt.figure(figsize=(12, 12)) 
    sns.heatmap(
        monthly_df,
        cmap="YlGnBu",
        cbar_kws={"label": "Days Present in Month"}
    )   
    plt.title("Monthly Attendance Heatmap")
    plt.xlabel("Months")    
    plt.ylabel("Stu    python d:\college\Attendance\main.py    python d:\college\Attendance\main.py    python d:\college\Attendance\main.pydents")
    monthly_heatmap_path = "monthly_attendance_heatmap.png"
    plt.savefig(monthly_heatmap_path)           
    plt.close()
    
    # top 10 regular and top 10 irregular students
    top_10 = df.sort_values("Attendance_Percentage", ascending=False).head(10)
    bottom_10 = df.sort_values("Attendance_Percentage").head(10)
    
    print(top_10[["Attendance_Percentage"]])
    print(bottom_10[["Attendance_Percentage"]])
    # Prepare DataFrames for Gradio outputs (reset index so 'Student' is a column)
    data_preview_df = df.reset_index()
    chronic_table_df = chronic_absentees.reset_index()[["Student", "Attendance_Percentage"]]
    eligible_table_df = regular_absentees.reset_index()[["Student", "Attendance_Percentage"]]

    # Return data and image file paths for Gradio
    return (
        data_preview_df,
        chronic_table_df,
        eligible_table_df,
        daily_heatmap_path,
        distribution_path,
        monthly_heatmap_path,
        monthly_bar_path,
    )
#  GRADIO UI
with gr.Blocks(title="Student Attendance Analysis System") as app:
    gr.Markdown("## 🎓 Student Attendance Analysis Dashboard")
    gr.Markdown("Upload your attendance CSV file to get full analysis.")

    file_input = gr.File(label="Upload Attendance CSV")

    run_btn = gr.Button("Run Analysis")

    data_preview = gr.Dataframe(label=" Data Preview")
    chronic_table = gr.Dataframe(label=" Chronic Absentees (<60%)")
    eligible_table = gr.Dataframe(label=" Eligible Students (≥75%)")

    daily_heatmap = gr.Image(label=" Daily Attendance Heatmap")
    distribution_plot = gr.Image(label=" Attendance Distribution")
    monthly_heatmap = gr.Image(label="Monthly Heatmap")
    monthly_bar = gr.Image(label="Monthly Attendance Bar Chart")

    run_btn.click(
        analyze_attendance,
        inputs=file_input,
        outputs=[
            data_preview,
            chronic_table,
            eligible_table,
            daily_heatmap,
            distribution_plot,
            monthly_heatmap,
            monthly_bar
        ]
    )

app.launch()