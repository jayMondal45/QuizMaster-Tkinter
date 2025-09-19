import requests
import html
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ------------------- Modern Color Scheme ------------------- #
COLORS = {
    'primary': '#4f46e5',      # Indigo
    'primary_hover': '#4338ca',
    'secondary': '#f8fafc',    # Light gray
    'accent': '#10b981',       # Green
    'danger': '#ef4444',       # Red
    'warning': '#f59e0b',      # Orange
    'dark': '#1e293b',         # Dark blue-gray
    'light': '#ffffff',
    'text': '#334155',
    'muted': '#64748b',
    'background': '#f1f5f9',   # Light blue-gray
    'card_bg': '#ffffff',      # Card background
    'card_shadow': '#e2e8f0'   # Card shadow
}

# ------------------- Beautiful Modal Dialog ------------------- #
class BeautifulModal:
    def __init__(self, parent, title, message, modal_type="info", details=None):
        self.parent = parent
        self.title = title
        self.message = message
        self.modal_type = modal_type
        self.details = details
        
        # Create modal window
        self.modal = tk.Toplevel(parent)
        self.modal.title(title)
        self.modal.geometry("400x250")
        self.modal.resizable(False, False)
        self.modal.configure(bg=COLORS['background'])
        self.modal.transient(parent)
        self.modal.grab_set()
        
        # Center the modal
        self.center_modal()
        
        # Set modal icon based on type
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "question": "❓"
        }
        self.icon = icons.get(modal_type, "ℹ️")
        
        self.create_widgets()
        
    def center_modal(self):
        """Center the modal on the screen"""
        self.modal.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (400 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (250 // 2)
        self.modal.geometry(f"400x250+{x}+{y}")
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.modal, bg=COLORS['card_bg'], relief=tk.RAISED, bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with icon and title
        header_frame = tk.Frame(main_frame, bg=COLORS['card_bg'])
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        icon_label = tk.Label(
            header_frame, text=self.icon, 
            font=("Arial", 24), bg=COLORS['card_bg'], fg=self.get_icon_color()
        )
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            header_frame, text=self.title, 
            font=("Arial", 16, "bold"), bg=COLORS['card_bg'], fg=COLORS['text']
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Message
        message_frame = tk.Frame(main_frame, bg=COLORS['card_bg'])
        message_frame.pack(fill=tk.X, padx=20, pady=10)
        
        message_label = tk.Label(
            message_frame, text=self.message, 
            font=("Arial", 12), bg=COLORS['card_bg'], fg=COLORS['text'],
            wraplength=350, justify=tk.LEFT
        )
        message_label.pack(anchor=tk.W)
        
        # Details if provided
        if self.details:
            details_frame = tk.Frame(main_frame, bg=COLORS['card_bg'])
            details_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
            
            details_label = tk.Label(
                details_frame, text=self.details, 
                font=("Arial", 10), bg=COLORS['card_bg'], fg=COLORS['muted'],
                wraplength=350, justify=tk.LEFT
            )
            details_label.pack(anchor=tk.W)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS['card_bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        ok_button = tk.Button(
            button_frame, text="OK", command=self.modal.destroy,
            font=("Arial", 12, "bold"), bg=self.get_button_color(), fg=COLORS['light'],
            relief='flat', padx=20, pady=5, cursor='hand2',
            activebackground=self.get_button_hover_color()
        )
        ok_button.pack()
        
    def get_icon_color(self):
        colors = {
            "info": COLORS['primary'],
            "success": COLORS['accent'],
            "warning": COLORS['warning'],
            "error": COLORS['danger'],
            "question": COLORS['primary']
        }
        return colors.get(self.modal_type, COLORS['primary'])
        
    def get_button_color(self):
        colors = {
            "info": COLORS['primary'],
            "success": COLORS['accent'],
            "warning": COLORS['warning'],
            "error": COLORS['danger'],
            "question": COLORS['primary']
        }
        return colors.get(self.modal_type, COLORS['primary'])
        
    def get_button_hover_color(self):
        colors = {
            "info": COLORS['primary_hover'],
            "success": '#0da271',
            "warning": '#e69008',
            "error": '#dc2626',
            "question": COLORS['primary_hover']
        }
        return colors.get(self.modal_type, COLORS['primary_hover'])

# ------------------- Fetch categories ------------------- #
def fetch_categories():
    try:
        CATEGORY_URL = "https://opentdb.com/api_category.php"
        response = requests.get(CATEGORY_URL, timeout=10)
        response.raise_for_status()
        categories_data = response.json()["trivia_categories"]
        return {cat["name"]: cat["id"] for cat in categories_data}
    except requests.RequestException:
        # Use BeautifulModal instead of messagebox
        return {
            "General Knowledge": 9,
            "Entertainment: Books": 10,
            "Entertainment: Film": 11,
            "Entertainment: Music": 12,
            "Science & Nature": 17,
            "Computers": 18,
            "Mathematics": 19,
            "Mythology": 20,
            "Sports": 21,
            "Geography": 22,
            "History": 23,
            "Animals": 27,
            "Vehicles": 28
        }

# ------------------- Quiz Settings Window ------------------- #
class QuizSettingsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Settings")
        self.root.config(bg=COLORS['background'])
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        
        # Variables to store user selections
        self.category_var = tk.StringVar()
        self.type_var = tk.StringVar(value="multiple")
        self.count_var = tk.StringVar(value="10")
        
        self.category_map = fetch_categories()
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"500x600+{x}+{y}")
        
    def create_widgets(self):
        # Create a canvas and scrollbar for the settings window
        canvas = tk.Canvas(self.root, bg=COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main frame with a subtle shadow effect
        main_frame = tk.Frame(scrollable_frame, bg=COLORS['card_shadow'], padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inner frame with white background
        inner_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief=tk.RAISED, bd=1)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with decorative elements
        title_frame = tk.Frame(inner_frame, bg=COLORS['primary'], height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, text="🧠 Quiz Settings", 
            font=("Arial", 20, "bold"), 
            bg=COLORS['primary'], fg=COLORS['light']
        )
        title_label.pack(expand=True)
        
        # Content area with padding
        content_frame = tk.Frame(inner_frame, bg=COLORS['card_bg'], padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Category selection
        category_frame = tk.Frame(content_frame, bg=COLORS['card_bg'])
        category_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            category_frame, text="Category:", 
            font=("Arial", 12, "bold"), bg=COLORS['card_bg'], fg=COLORS['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Sort categories alphabetically
        sorted_categories = sorted(self.category_map.keys())
        self.category_combo = ttk.Combobox(
            category_frame, values=sorted_categories, 
            width=40, state="readonly", font=("Arial", 10), textvariable=self.category_var
        )
        self.category_combo.pack(fill=tk.X, pady=5)
        self.category_combo.set("Entertainment: Film")  # Default selection
        
        # Question type selection
        type_frame = tk.Frame(content_frame, bg=COLORS['card_bg'])
        type_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            type_frame, text="Question Type:", 
            font=("Arial", 12, "bold"), bg=COLORS['card_bg'], fg=COLORS['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        type_options_frame = tk.Frame(type_frame, bg=COLORS['card_bg'])
        type_options_frame.pack(fill=tk.X, pady=5)
        
        # Radio buttons with different colors
        types = [("Multiple Choice", "multiple", COLORS['primary']), 
                ("True/False", "boolean", COLORS['accent'])]
        
        for text, value, color in types:
            rb = tk.Radiobutton(
                type_options_frame, text=text, variable=self.type_var,
                value=value, bg=COLORS['card_bg'], fg=COLORS['text'],
                selectcolor=color, font=("Arial", 10), 
                activebackground=COLORS['card_bg']
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Number of questions selection
        count_frame = tk.Frame(content_frame, bg=COLORS['card_bg'])
        count_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            count_frame, text="Number of Questions:", 
            font=("Arial", 12, "bold"), bg=COLORS['card_bg'], fg=COLORS['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        count_options_frame = tk.Frame(count_frame, bg=COLORS['card_bg'])
        count_options_frame.pack(fill=tk.X, pady=5)
        
        # Radio buttons with different colors for 5, 10, 15, and 20 questions
        counts = [("5", "5", "#FF9999"), 
                 ("10", "10", "#99CCFF"), 
                 ("15", "15", "#99FF99"),
                 ("20", "20", "#FFCC99")]
        
        for text, value, color in counts:
            rb = tk.Radiobutton(
                count_options_frame, text=text, variable=self.count_var,
                value=value, bg=COLORS['card_bg'], fg=COLORS['text'],
                selectcolor=color, font=("Arial", 10), 
                activebackground=COLORS['card_bg']
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Start button with attractive styling
        button_frame = tk.Frame(content_frame, bg=COLORS['card_bg'])
        button_frame.pack(fill=tk.X, pady=20)
        
        start_button = tk.Button(
            button_frame, text="🚀 Start Quiz", command=self.start_quiz,
            font=("Arial", 14, "bold"), bg=COLORS['primary'], fg=COLORS['light'],
            relief='flat', padx=30, pady=12, cursor='hand2',
            activebackground=COLORS['primary_hover']
        )
        start_button.pack(fill=tk.X)
        
        # Make sure the canvas is scrollable
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def start_quiz(self):
        """Start the quiz with selected settings"""
        selected_category = self.category_var.get()
        if not selected_category:
            # Use BeautifulModal instead of messagebox
            BeautifulModal(self.root, "Missing Selection", "Please select a category first!", "warning")
            return
            
        # Get selected values
        category_id = self.category_map[selected_category]
        question_type = self.type_var.get()
        question_count = int(self.count_var.get())
        
        # Close settings window and open quiz window
        self.root.destroy()
        
        # Create quiz window
        quiz_app = QuizWindow(category_id, question_type, question_count)
        quiz_app.run()
        
    def run(self):
        """Run the settings window"""
        self.root.mainloop()

# ------------------- Quiz Window ------------------- #
class QuizWindow:
    def __init__(self, category_id, question_type, question_count):
        self.root = tk.Tk()
        self.category_id = category_id
        self.question_type = question_type
        self.question_count = question_count
        self.question_list = []
        self.current_index = 0
        self.current_score = 0
        
        self.setup_ui()
        self.fetch_questions()
        
    def setup_ui(self):
        self.root.title("Quiz Time!")
        self.root.config(bg=COLORS['background'])
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        
        # Header with score
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        self.score_label = tk.Label(
            header_frame, text="Score: 0", 
            font=("Arial", 14, "bold"), 
            bg=COLORS['primary'], fg=COLORS['light']
        )
        self.score_label.pack(side=tk.RIGHT, padx=20)
        
        # Question display
        self.question_frame = tk.Frame(self.root, bg=COLORS['card_bg'], relief=tk.RAISED, bd=1)
        self.question_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.question_label = tk.Label(
            self.question_frame, text="Loading questions...", 
            font=("Arial", 14), bg=COLORS['card_bg'], fg=COLORS['text'],
            wraplength=500, justify=tk.CENTER
        )
        self.question_label.pack(expand=True, padx=20, pady=20)
        
        # Answer buttons frame
        self.answer_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.answer_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Progress label
        self.progress_label = tk.Label(
            self.root, text="Question 0/0", 
            font=("Arial", 10), bg=COLORS['background'], fg=COLORS['muted']
        )
        self.progress_label.pack(pady=(0, 10))
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
    def fetch_questions(self):
        """Fetch questions from the API"""
        try:
            url = f"https://opentdb.com/api.php?amount={self.question_count}&category={self.category_id}&type={self.question_type}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("response_code", 1) != 0:
                BeautifulModal(self.root, "API Error", "No questions found for these settings.", "error")
                self.root.destroy()
                return
                
            questions = data["results"]
            self.question_list.clear()
            
            for q in questions:
                question_text = html.unescape(q["question"])
                correct_answer = html.unescape(q["correct_answer"])
                incorrect_answers = [html.unescape(ans) for ans in q["incorrect_answers"]]
                
                if q["type"] == "multiple":
                    all_answers = incorrect_answers + [correct_answer]
                    random.shuffle(all_answers)
                    self.question_list.append((question_text, correct_answer, all_answers))
                else:
                    self.question_list.append((question_text, correct_answer, ["True", "False"]))
            
            if not self.question_list:
                BeautifulModal(self.root, "Error", "No questions found for these settings.", "error")
                self.root.destroy()
                return
                
            self.show_question()
            
        except requests.RequestException:
            BeautifulModal(self.root, "Connection Error", "Failed to fetch questions. Please check your internet connection.", "error")
            self.root.destroy()
    
    def show_question(self):
        """Display the current question"""
        if self.current_index >= len(self.question_list):
            self.show_results()
            return
            
        # Update progress
        self.progress_label.config(text=f"Question {self.current_index + 1}/{len(self.question_list)}")
        
        # Clear previous answer buttons
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
            
        # Get current question data
        question_data = self.question_list[self.current_index]
        question_text = question_data[0]
        correct_answer = question_data[1]
        all_answers = question_data[2]
        
        # Display question
        self.question_label.config(text=question_text)
        
        # Create answer buttons based on question type
        if self.question_type == "boolean":
            # True/False buttons
            true_button = tk.Button(
                self.answer_frame, text="TRUE", command=lambda: self.check_answer("True", correct_answer),
                font=("Arial", 12, "bold"), bg=COLORS['accent'], fg=COLORS['light'],
                relief='flat', padx=20, pady=10, cursor='hand2',
                activebackground='#059669'
            )
            true_button.pack(side=tk.LEFT, expand=True, padx=5)
            
            false_button = tk.Button(
                self.answer_frame, text="FALSE", command=lambda: self.check_answer("False", correct_answer),
                font=("Arial", 12, "bold"), bg=COLORS['danger'], fg=COLORS['light'],
                relief='flat', padx=20, pady=10, cursor='hand2',
                activebackground='#dc2626'
            )
            false_button.pack(side=tk.RIGHT, expand=True, padx=5)
        else:
            # Multiple choice buttons with distinct colors
            colors = ['#99CCFF', '#99FF99', '#FF9999', '#FFFF99']
            for i, answer in enumerate(all_answers):
                btn = tk.Button(
                    self.answer_frame, text=answer, 
                    command=lambda ans=answer: self.check_answer(ans, correct_answer),
                    font=("Arial", 10), bg=colors[i], fg=COLORS['text'],
                    relief='flat', padx=15, pady=8, cursor='hand2',
                    activebackground=colors[i],
                    wraplength=120, justify='center'
                )
                btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
                
            # Configure grid to expand properly
            for i in range(2):
                self.answer_frame.grid_columnconfigure(i, weight=1)
            for i in range(2):
                self.answer_frame.grid_rowconfigure(i, weight=1)
    
    def check_answer(self, user_answer, correct_answer):
        """Check if the user's answer is correct"""
        if user_answer == correct_answer:
            self.current_score += 1
            self.score_label.config(text=f"Score: {self.current_score}")
            BeautifulModal(self.root, "Correct! 🎉", "Your answer is correct!", "success")
        else:
            BeautifulModal(self.root, "Incorrect 😞", f"Sorry, the correct answer was: {correct_answer}", "error")
        
        # Move to next question after modal is closed
        self.root.after(100, self.next_question)
    
    def next_question(self):
        """Move to the next question"""
        self.current_index += 1
        self.show_question()
    
    def show_results(self):
        """Show the final results"""
        # Clear the question and answer frames
        self.question_label.config(text="")
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
            
        # Calculate percentage
        percentage = (self.current_score / len(self.question_list)) * 100
        
        # Performance message
        if percentage >= 80:
            performance = "Outstanding! 🏆"
            color = COLORS['accent']
            modal_type = "success"
        elif percentage >= 60:
            performance = "Good job! 👍"
            color = COLORS['primary']
            modal_type = "info"
        elif percentage >= 40:
            performance = "Keep learning! 📚"
            color = COLORS['warning']
            modal_type = "warning"
        else:
            performance = "Try again! 💪"
            color = COLORS['danger']
            modal_type = "error"
            
        # Display results
        result_text = f"Quiz Complete!\n\n{performance}\n\nFinal Score: {self.current_score}/{len(self.question_list)}\nPercentage: {percentage:.1f}%"
        result_label = tk.Label(
            self.question_frame, text=result_text,
            font=("Arial", 14, "bold"), bg=COLORS['card_bg'], fg=color,
            justify=tk.CENTER
        )
        result_label.pack(expand=True)
        
        # Add a restart button
        restart_button = tk.Button(
            self.answer_frame, text="New Quiz", command=self.restart_quiz,
            font=("Arial", 12, "bold"), bg=COLORS['primary'], fg=COLORS['light'],
            relief='flat', padx=20, pady=8, cursor='hand2',
            activebackground=COLORS['primary_hover']
        )
        restart_button.pack(expand=True, pady=10)
    
    def restart_quiz(self):
        """Restart the quiz by going back to settings"""
        self.root.destroy()
        settings_app = QuizSettingsWindow()
        settings_app.run()
        
    def run(self):
        """Run the quiz window"""
        self.root.mainloop()

# ------------------- Main Application ------------------- #
if __name__ == "__main__":
    settings_app = QuizSettingsWindow()
    settings_app.run()