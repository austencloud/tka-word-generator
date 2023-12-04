import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QMessageBox
import enchant
from functions import Interpolation
from data import start_letters, positions

class InterpolationGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.interpolation = Interpolation(start_letters, positions)
        self.dictionary = enchant.Dict("en_US")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Word Generator')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Length input
        length_label = QLabel("Enter length of the word:")
        self.length_entry = QLineEdit()
        layout.addWidget(length_label)
        layout.addWidget(self.length_entry)

        # Generate button
        generate_button = QPushButton("Generate Words")
        generate_button.clicked.connect(self.generate_words)
        layout.addWidget(generate_button)

        # Valid words
        valid_word_label = QLabel("Words:")
        valid_word_label.setStyleSheet("font-size: 15px;")
        self.word_text = QTextEdit()
        layout.addWidget(valid_word_label)
        layout.addWidget(self.word_text)

        # Real words
        real_word_label = QLabel("Real Words:")
        real_word_label.setStyleSheet("font-size: 15px;")
        self.real_words_text = QTextEdit()
        layout.addWidget(real_word_label)
        layout.addWidget(self.real_words_text)

        # Word count
        self.word_count_label = QLabel("Words generated: 0")
        layout.addWidget(self.word_count_label)

        # Circular checkbox
        self.circular_checkbox = QCheckBox("Circular words")
        layout.addWidget(self.circular_checkbox)

    def generate_words(self):
        try:
            length = int(self.length_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Invalid input", "Please enter a valid number")
            return

        valid_words = self.interpolation.generate_all_valid_words(length)
        valid_words.sort()

        real_words = [word for word in valid_words if self.dictionary.check(word)]

        self.word_text.clear()
        self.real_words_text.clear()

        for word in valid_words:
            self.word_text.append(word)
        for word in real_words:
            self.real_words_text.append(word)

        self.word_count_label.setText(f"Words generated: {len(valid_words)}")

    def generate_all_valid_words(self, length):
        circular = self.circular_checkbox.isChecked()
        return self.interpolation.generate_all_valid_words(length, circular)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = InterpolationGUI()
    ex.show()
    sys.exit(app.exec())
