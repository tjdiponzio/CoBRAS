import random
import tkinter as tk
from tkinter import messagebox


class SurveyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Likert Scale Survey")
        self.root.geometry("950x650")

        # --- Scale Configuration ---
        self.max_scale_value = 6
        self.likert_options = [
            ("Strongly Disagree", 1),
            ("", 2),
            ("", 3),
            ("", 4),
            ("", 5),
            ("Strongly Agree", 6),
        ]

        # --- Data Structure ---
        # CoBRAS Scale questions mapped to subscales
        base_questions = [
            {
                "text": "Everyone who works hard, no matter what race they are, has an equal chance to become rich.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": False,
            },
            {
                "text": "Race plays a major role in the type of social services (such as type of health care or day care) that people receive in the U.S",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "Race is very important in determining who is successful and who is not.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "Racial and ethnic minorities do not have the same opportunities as White people in the U.S.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "White people in the U.S. have certain advantages because of the color of their skin.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "White people are more to blame for racial discrimination in the U.S. than racial and ethnic minorities.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "Race plays an important role in who gets sent to prison.",
                "subscale": "Unawareness of Racial Privilege",
                "reverse": True,
            },
            {
                "text": "It is important that people begin to think of themselves as American and not African American, Mexican American or Italian American.",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "Due to racial discrimination, programs such as affirmative action are necessary to help create equality.",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": True,
            },
            {
                "text": "White people in the U.S. are discriminated against because of the color their skin",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "Immigrants should try to fit into the culture and adopt the values of the U.S",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "English should be the only official language in the U.S.",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "Social policies, such as affirmative action, discriminate unfairly against White people.",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "Racial and ethnic minorities in the U.S. have certain advantages because of the color of their skin.",
                "subscale": "Unawareness of Institutional Discrimination",
                "reverse": False,
            },
            {
                "text": "Racism is a major problem in the U.S.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": True,
            },
            {
                "text": "Racism may have been a problem in the past, but it is not an important problem today.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": False,
            },
            {
                "text": "Talking about racial issues causes unnecessary tension.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": False,
            },
            {
                "text": "It is important for political leaders to talk about racism to help work through or solve society’s problems.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": True,
            },
            {
                "text": "It is important for public schools to teach about the history and contributions of racial and ethnic minorities.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": True,
            },
            {
                "text": "Racial problems in the U.S. are rare, isolated situations.",
                "subscale": "Unawareness to Blatant Racial Issues",
                "reverse": False,
            },
        ]

        # Randomize the question list upon initialization
        self.questions = list(base_questions)
        random.shuffle(self.questions)

        # Track UI variables
        self.answer_vars = []
        self.progress_text_var = tk.StringVar(
            value=f"0 / {len(self.questions)} Answered"
        )

        # --- Layout ---
        self.left_frame = tk.Frame(root, padx=30, pady=20)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(
            root,
            width=280,
            bg="#f8f9fa",
            padx=20,
            pady=20,
            borderwidth=1,
            relief="solid",
        )
        self.right_frame.pack(side="right", fill="y")
        self.right_frame.pack_propagate(False)

        self.setup_left_panel()
        self.setup_right_panel()

    def setup_left_panel(self):
        tk.Label(
            self.left_frame, text="SURVEY QUESTIONNAIRE", font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 20))

        # Scrollable area setup
        canvas = tk.Canvas(self.left_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            self.left_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Generate Likert Rows
        for i, q in enumerate(self.questions):
            row_container = tk.Frame(
                self.scrollable_frame, pady=15, borderwidth=1, relief="flat"
            )
            row_container.pack(fill="x", anchor="w")

            label_text = f"{i + 1}. {q['text']}"

            tk.Label(
                row_container,
                text=label_text,
                font=("Helvetica", 11, "bold"),
                wraplength=550,
                justify="left",
            ).pack(anchor="w")

            options_frame = tk.Frame(row_container)
            options_frame.pack(fill="x", pady=5)

            var = tk.IntVar(value=0)
            self.answer_vars.append(var)

            for opt_text, points in self.likert_options:
                rb = tk.Radiobutton(
                    options_frame,
                    text=opt_text,
                    variable=var,
                    value=points,
                    command=self.update_progress,
                    font=("Helvetica", 9),
                )
                rb.pack(side="left", padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_right_panel(self):
        tk.Label(
            self.right_frame,
            text="Survey Progress",
            font=("Helvetica", 12, "bold"),
            bg="#f8f9fa",
        ).pack(pady=10)

        interpretation = "Please respond to all statements\nhonestly. Your total score breakdown\nwill be shown here at the end."
        tk.Label(
            self.right_frame,
            text=interpretation,
            justify="center",
            bg="#f8f9fa",
            font=("Helvetica", 10),
        ).pack(pady=10)

        tk.Frame(self.right_frame, height=1, bg="#dee2e6").pack(
            fill="x", pady=10
        )

        tk.Label(
            self.right_frame, text="COMPLETION", font=("Helvetica", 11), bg="#f8f9fa"
        ).pack()
        self.progress_display = tk.Label(
            self.right_frame,
            textvariable=self.progress_text_var,
            font=("Helvetica", 20, "bold"),
            fg="#6c757d",
            bg="#f8f9fa",
        )
        self.progress_display.pack(pady=20)

        # Store submit button as instance variable so we can change its behavior on results screen
        self.submit_btn = tk.Button(
            self.right_frame,
            text="Submit Survey",
            command=self.submit,
            bg="#28a745",
            fg="white",
            font=("Helvetica", 10, "bold"),
            pady=10,
        )
        self.submit_btn.pack(side="bottom", fill="x")

    def update_progress(self):
        answered_count = sum(1 for var in self.answer_vars if var.get() != 0)
        self.progress_text_var.set(
            f"{answered_count} / {len(self.questions)} Answered"
        )

        if answered_count == len(self.questions):
            self.progress_display.config(fg="#007bff")
        else:
            self.progress_display.config(fg="#6c757d")

    def calculate_scores(self):
        """Calculates total, subscale scores, and dynamic score ranges based on question counts."""
        total_score = 0
        subscale_scores = {}
        subscale_counts = {}

        # First pass: count questions per subscale to determine the ranges automatically
        for q in self.questions:
            sub = q["subscale"]
            subscale_counts[sub] = subscale_counts.get(sub, 0) + 1
            if sub not in subscale_scores:
                subscale_scores[sub] = 0

        # Second pass: calculate values
        for i, q in enumerate(self.questions):
            raw_val = self.answer_vars[i].get()
            if raw_val == 0:
                continue

            actual_val = (
                (self.max_scale_value + 1) - raw_val if q["reverse"] else raw_val
            )
            total_score += actual_val
            subscale_scores[q["subscale"]] += actual_val

        # Create structured subscale results data with dynamic range maps
        subscale_results = {}
        for sub, score in subscale_scores.items():
            count = subscale_counts[sub]
            min_possible = count * 1
            max_possible = count * self.max_scale_value
            subscale_results[sub] = {
                "score": score,
                "range_str": f"{min_possible} - {max_possible}",
            }

        # Global range configuration
        total_range_str = f"{len(self.questions) * 1} - {len(self.questions) * self.max_scale_value}"

        return total_score, total_range_str, subscale_results

    def display_results_screen(self, final_total, total_range, subscales):
        """Wipes out the questionnaire and draws the final evaluation view on the same window."""
        # Destroy all layout contents in the left window frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Title Block
        tk.Label(
            self.left_frame, text="EVALUATION RESULTS", font=("Helvetica", 16, "bold"), fg="#343a40"
        ).pack(pady=(0, 10))

        # Clinical Guidance Note
        note_text = "Note: Higher scores indicate areas you should consider evaluating further after meeting with your client."
        tk.Label(
            self.left_frame, text=note_text, font=("Helvetica", 10, "italic"), fg="#6c757d", wraplength=550,
            justify="left"
        ).pack(pady=(0, 20), anchor="w")

        # Container Frame for Scores
        results_container = tk.Frame(self.left_frame)
        results_container.pack(fill="both", expand=True)

        # Render Total Score Card
        total_card = tk.LabelFrame(results_container, text=" Overall Score ", font=("Helvetica", 11, "bold"), padx=15,
                                   pady=10)
        total_card.pack(fill="x", pady=(0, 15))
        tk.Label(total_card, text=f"Total Score: {final_total}", font=("Helvetica", 13, "bold"), fg="#007bff").pack(
            side="left")
        tk.Label(total_card, text=f"(Possible Range: {total_range})", font=("Helvetica", 10), fg="#6c757d").pack(
            side="right")

        # Render Subscale Breakdowns
        for subscale, data in subscales.items():
            card = tk.LabelFrame(results_container, text=f" {subscale} ", font=("Helvetica", 11, "bold"), padx=15,
                                 pady=10)
            card.pack(fill="x", pady=5)

            tk.Label(card, text=f"Score: {data['score']}", font=("Helvetica", 12, "bold"), fg="#495057").pack(
                side="left")
            tk.Label(card, text=f"(Scale Range: {data['range_str']})", font=("Helvetica", 10), fg="#6c757d").pack(
                side="right")

        # Update right panel to clean up completion text and switch button actions
        self.progress_text_var.set("Complete")
        self.progress_display.config(fg="#28a745")
        self.submit_btn.config(text="Close Application", command=self.root.destroy, bg="#dc3545")

    def submit(self):
        if any(var.get() == 0 for var in self.answer_vars):
            messagebox.showwarning(
                "Incomplete", "Please answer all questions before submitting."
            )
            return

        final_total, total_range, subscales = self.calculate_scores()

        # Render results inline instead of popping up a dialog window
        self.display_results_screen(final_total, total_range, subscales)


if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()