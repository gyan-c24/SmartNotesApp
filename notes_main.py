#start to create smart notes app
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QTextEdit, QInputDialog
import json

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Smart Notes")
main_window.resize(900, 600)
layout_main = QHBoxLayout()
main_window.setLayout(layout_main)

#Left side
edit_text = QTextEdit()
layout_left = QHBoxLayout()
layout_left.addWidget(edit_text)

#Top half (right)
layout_note = QVBoxLayout()
label_note = QLabel()
label_note.setText("List of notes")
layout_note.addWidget(label_note)
list_note = QListWidget()
layout_note.addWidget(list_note)

def show_note():
    key = list_note.selectedItems()[0].text()
    t = note_dictionary[key]["text"]
    edit_text.setText(t)
    t = note_dictionary[key]["tags"]
    list_tag.clear()
    list_tag.addItems(t)
list_note.itemClicked.connect(show_note)

layout_button_note = QHBoxLayout()
layout_note.addLayout(layout_button_note)
button_create = QPushButton()
button_create.setText("Create note")
def add_note():
    note_name, result = QInputDialog.getText(main_window, "Add note", "Note name")
    if result == True:
        note_dictionary[note_name] = {"tags" : [], "text" : ""}
        list_note.clear()
        list_note.addItems(note_dictionary.keys())
button_create.clicked.connect(add_note)
layout_button_note.addWidget(button_create)
button_delete = QPushButton()
button_delete.setText("Delete note")
def delete_note():
    key = list_note.selectedItems()[0].text()
    del note_dictionary[key]
    list_note.clear()
    list_note.addItems(note_dictionary.keys())
    list_tag.clear()
    edit_text.clear()
button_delete.clicked.connect(delete_note) 
layout_button_note.addWidget(button_delete)
button_save = QPushButton()
button_save.setText("Save note")
def save_note():
    if len(list_note.selectedItems()) != 0:
        key = list_note.selectedItems()[0].text()
        text = edit_text.toPlainText()
        note_dictionary[key]["text"] = text
    with open("notes_data.json", "w") as file:
        json.dump(note_dictionary, file)
        file.close()
button_save.clicked.connect(save_note)
layout_note.addWidget(button_save)

#Bottom half (right)
layout_tag = QVBoxLayout()
label_tag = QLabel()
label_tag.setText("List of tags")
layout_tag.addWidget(label_tag)
list_tag = QListWidget()
layout_tag.addWidget(list_tag)
edit_tag = QLineEdit()
edit_tag.setPlaceholderText("Enter tag...")
layout_tag.addWidget(edit_tag)
layout_button_tag = QHBoxLayout()
layout_tag.addLayout(layout_button_tag)
button_add = QPushButton()
button_add.setText("Add to note")
def add_tag():
    key = list_note.selectedItems()[0].text()
    tag = edit_tag.text()
    if tag not in note_dictionary[key]["tags"]:
        note_dictionary[key]["tags"].append(tag)
        tags = note_dictionary[key]["tags"]
        list_tag.clear()
        list_tag.addItems(tags)
button_add.clicked.connect(add_tag)    
layout_button_tag.addWidget(button_add)
button_untag = QPushButton()
button_untag.setText("Untag from note")
def untag():
    key = list_note.selectedItems()[0].text()
    tag = list_tag.selectedItems()[0].text()
    note_dictionary[key]["tags"].remove(tag)
    list_tag.clear()
    list_tag.addItems(note_dictionary[key]["tags"])
button_untag.clicked.connect(untag)
layout_button_tag.addWidget(button_untag)
button_search = QPushButton()
button_search.setText("Search notes by tag")
def search_notes():
    tag = edit_tag.text()
    for key in note_dictionary.keys():
        if tag in note_dictionary[key]["tags"]:
            t = note_dictionary[key]["text"]
            edit_text.setText(t)
            t = note_dictionary[key]["tags"]
            list_tag.clear()
            list_tag.addItems(t)
button_search.clicked.connect(search_notes)
layout_tag.addWidget(button_search)

#Right side
layout_right = QVBoxLayout()
layout_right.addLayout(layout_note)
layout_right.addLayout(layout_tag)

#Combine
layout_main.addLayout(layout_left, stretch = 2)
layout_main.addLayout(layout_right, stretch = 1)

with open("notes_data.json", "r") as file:
    note_dictionary = json.load(file)
    print(note_dictionary)
list_note.addItems(note_dictionary.keys())

main_window.setLayout(layout_main)
main_window.show()
app.exec_()