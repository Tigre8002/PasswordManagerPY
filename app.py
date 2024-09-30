import flet as ft
import pyperclip 

class App:
    def __init__(self, page: ft.Page):
        self.page = page   
        
        page.appbar = ft.AppBar(
            title=ft.Text("Password Manager", color=ft.colors.BLACK87),
            bgcolor=ft.colors.RED_300,
            center_title=True,
            color=ft.colors.WHITE,
        )
        
        page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.addPassword,bgcolor=ft.colors.BLUE_100)
        
        self.loadAllBoards()
        
    def addPassword(self, e):
        passwordText = ft.TextField(label="Password", password=True, can_reveal_password=True)
        nameText = ft.TextField(label="Name")
        
        def deleteBoardPassword(e=None):
            Board.visible = False
            self.page.update()
            
        def addBoard(e):
            deleteBoardPassword()
            
            passwordToSave = passwordText.value
            nameToSave = nameText.value
            
            self.createBoard(nameToSave, passwordToSave)
            
        Board = ft.Container(content=ft.Row(
            [
                nameText,
                passwordText,
                ft.IconButton(ft.icons.ADD, on_click=addBoard),
                ft.IconButton(ft.icons.REMOVE, on_click=deleteBoardPassword),
            ], ft.MainAxisAlignment.CENTER), width=900, height=80, alignment=ft.alignment.center)
        
        self.page.add(Board)
        
        
    def createBoard(self, name, passwordText, hasSave = None):
        password = passwordText
        
        nameBoardComp = ft.Text(value=name, size=40, color=ft.colors.BLUE_400)
        
        nameToChange = ft.TextField(label="Name", value=name)
        passwordToChange = ft.TextField(label="Password", value=password)   
        
        colorsSettingsName = [ft.colors.RED, ft.colors.GREEN, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PURPLE, ft.colors.ORANGE]
        
        def copyBoard(e):
            pyperclip.copy(password)
            print(password)
            
        def deleteBoard(e):
            self.deleteBoard(name, password)
            Board.visible = False
            self.page.update()  
            
        def openSettingsBoard(e):
            colorTextToChange = nameBoardComp.color
            
            def closeDialog(e = None):
                dlg.open = False
                self.page.update()
                
                colorTextToChange = None
                
            def applySettings(e):
                nonlocal password
                
                self.changeBoard(nameBoardComp.value, password, nameToChange.value, passwordToChange.value)
                
                nameBoardComp.value = nameToChange.value
                password = passwordToChange.value
                
                nameBoardComp.color = colorTextToChange
                
                print(colorTextToChange)
                
                closeDialog()
                
            def setColorSettings(color):
                nonlocal colorTextToChange
                colorTextToChange = color
                
            def getColorsSettings():
                table = []
                
                for i in colorsSettingsName:
                    table.append(ft.Container(width=50, height=50,  bgcolor=i,border_radius=25, on_click=lambda e: setColorSettings(i)))
                    
                print(table)
                    
                return table
            
            colors = getColorsSettings()
                
            dlg = ft.AlertDialog(
                title=ft.Text("Settings Board"),
                content=ft.Column([
                    nameToChange,
                    passwordToChange,
                    ft.Row(colors)
                ], height=200),
                actions=[
                    ft.TextButton("Cancel", on_click=closeDialog),
                    ft.TextButton("Apply", on_click=applySettings)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            
        Board = ft.Container(ft.Draggable(
            content=ft.Row(
            [
                nameBoardComp,
                ft.Text(value="***********", size=30, color=ft.colors.PINK),
                ft.IconButton(ft.icons.CONTENT_COPY, on_click=copyBoard),
                ft.IconButton(ft.icons.REMOVE, on_click=deleteBoard),
                ft.IconButton(ft.icons.SETTINGS, on_click=openSettingsBoard),
            ], ft.MainAxisAlignment.CENTER)
        ))
            
        self.page.add(Board)
        
        if not hasSave:
            self.saveBoard(name, password)
            
        self.page.update()
        
        
    def loadAllBoards(self):
        if self.page.client_storage.get("list") == None: return
        
        list = self.page.client_storage.get("list")
        
        for i in list:
            self.createBoard(i[0], i[1], True)
        
        
    def saveBoard(self, name, password):
        if self.page.client_storage.get("list") is None: self.page.client_storage.set("list", [])
        
        list = self.page.client_storage.get("list")
        list.append([name, password])
        
        self.page.client_storage.set("list", list)
        
    def changeBoard(self, name, password, newName, newPassword):
        list = self.page.client_storage.get("list")
        indexTable = None
        
        for i in list:
            if i[0] == name:
                indexTable = list.index(i)
                
        list[indexTable][0] = newName
        list[indexTable][1] = newPassword
        
        self.page.client_storage.set("list", list)
        
    def deleteBoard(self, name, password):
        list = self.page.client_storage.get("list")
        
        for i in list:
            if i[0] == name:
                del list[list.index(i)]
                
        self.page.client_storage.set("list", list)