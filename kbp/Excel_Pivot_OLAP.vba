' ============================================================
' Excel VBA Makro - Automatsko kreiranje Pivot tabela iz OLAP kocke
' Seminarski: Data Warehouse IT kompanije, Ognjen Grgur
'
' UPUTSTVO:
' 1. Otvori Excel (prazan workbook)
' 2. Alt+F11 (otvara VBA editor)
' 3. Insert -> Module
' 4. Zalepi ceo ovaj kod
' 5. F5 (Run) ili Run -> Run Sub
' 6. Sacekaj par sekundi - kreira 4 pivot tabele + 2 grafikona
' ============================================================

Sub KreirajPivotTabele()

    Dim wb As Workbook
    Dim ws As Worksheet
    Dim pc As PivotCache
    Dim pt As PivotTable
    Dim connStr As String
    
    Set wb = ActiveWorkbook
    
    ' Connection string za Analysis Services
    connStr = "OLEDB;Provider=MSOLAP;Data Source=localhost;Initial Catalog=ITKompanijaDW_OLAP;"
    
    ' ==========================================
    ' PIVOT 1: Produktivnost po odeljenjima i godinama
    ' ==========================================
    Set ws = wb.Sheets.Add
    ws.Name = "Produktivnost_Odeljenja"
    
    Set pc = wb.PivotCaches.Create( _
        SourceType:=xlExternal, _
        SourceData:=connStr, _
        Version:=xlPivotTableVersion15)
    pc.CommandType = xlCmdCube
    pc.CommandText = "cbProduktivnost"
    
    Set pt = pc.CreatePivotTable( _
        TableDestination:=ws.Range("A3"), _
        TableName:="PT_Produktivnost_Odeljenja")
    
    ' Dodaj polja
    pt.CubeFields("[Odeljenje].[Odeljenje]").Orientation = xlRowField
    pt.CubeFields("[Godina].[Godina]").Orientation = xlColumnField
    pt.AddDataField pt.CubeFields("[Measures].[Broj Sati]")
    pt.AddDataField pt.CubeFields("[Measures].[Trosak Rada]")
    
    ' ==========================================
    ' PIVOT 2: Produktivnost po zaposlenima
    ' ==========================================
    Set ws = wb.Sheets.Add
    ws.Name = "Produktivnost_Zaposleni"
    
    Set pc = wb.PivotCaches.Create( _
        SourceType:=xlExternal, _
        SourceData:=connStr, _
        Version:=xlPivotTableVersion15)
    pc.CommandType = xlCmdCube
    pc.CommandText = "cbProduktivnost"
    
    Set pt = pc.CreatePivotTable( _
        TableDestination:=ws.Range("A3"), _
        TableName:="PT_Produktivnost_Zaposleni")
    
    pt.CubeFields("[Zaposleni].[Zaposleni]").Orientation = xlRowField
    pt.CubeFields("[Projekat].[Projekat]").Orientation = xlColumnField
    pt.AddDataField pt.CubeFields("[Measures].[Broj Sati]")
    
    ' ==========================================
    ' PIVOT 3: Prihodi po klijentima
    ' ==========================================
    Set ws = wb.Sheets.Add
    ws.Name = "Prihodi_Klijenti"
    
    Set pc = wb.PivotCaches.Create( _
        SourceType:=xlExternal, _
        SourceData:=connStr, _
        Version:=xlPivotTableVersion15)
    pc.CommandType = xlCmdCube
    pc.CommandText = "cbPrihodi"
    
    Set pt = pc.CreatePivotTable( _
        TableDestination:=ws.Range("A3"), _
        TableName:="PT_Prihodi_Klijenti")
    
    pt.CubeFields("[Klijent].[Klijent]").Orientation = xlRowField
    pt.CubeFields("[Godina].[Godina]").Orientation = xlColumnField
    pt.AddDataField pt.CubeFields("[Measures].[Iznos]")
    pt.AddDataField pt.CubeFields("[Measures].[Broj Faktura]")
    
    ' ==========================================
    ' PIVOT 4: Prihodi po projektima
    ' ==========================================
    Set ws = wb.Sheets.Add
    ws.Name = "Prihodi_Projekti"
    
    Set pc = wb.PivotCaches.Create( _
        SourceType:=xlExternal, _
        SourceData:=connStr, _
        Version:=xlPivotTableVersion15)
    pc.CommandType = xlCmdCube
    pc.CommandText = "cbPrihodi"
    
    Set pt = pc.CreatePivotTable( _
        TableDestination:=ws.Range("A3"), _
        TableName:="PT_Prihodi_Projekti")
    
    pt.CubeFields("[Projekat].[Projekat]").Orientation = xlRowField
    pt.CubeFields("[Kvartal].[Kvartal]").Orientation = xlColumnField
    pt.AddDataField pt.CubeFields("[Measures].[Iznos]")
    pt.AddDataField pt.CubeFields("[Measures].[Budzet]")
    
    ' ==========================================
    ' GRAFIKON 1: Produktivnost po odeljenjima (Bar Chart)
    ' ==========================================
    Dim ws1 As Worksheet
    Set ws1 = wb.Sheets("Produktivnost_Odeljenja")
    ws1.Activate
    
    Dim cht1 As Chart
    Set cht1 = wb.Charts.Add
    cht1.Name = "Grafikon_Produktivnost"
    cht1.SetSourceData ws1.PivotTables("PT_Produktivnost_Odeljenja").TableRange1
    cht1.ChartType = xlColumnClustered
    cht1.HasTitle = True
    cht1.ChartTitle.Text = "Produktivnost po odeljenjima"
    
    ' ==========================================
    ' GRAFIKON 2: Prihodi po klijentima (Bar Chart)
    ' ==========================================
    Dim ws3 As Worksheet
    Set ws3 = wb.Sheets("Prihodi_Klijenti")
    ws3.Activate
    
    Dim cht2 As Chart
    Set cht2 = wb.Charts.Add
    cht2.Name = "Grafikon_Prihodi"
    cht2.SetSourceData ws3.PivotTables("PT_Prihodi_Klijenti").TableRange1
    cht2.ChartType = xlColumnClustered
    cht2.HasTitle = True
    cht2.ChartTitle.Text = "Prihodi po klijentima"
    
    MsgBox "Gotovo! Kreirano:" & vbCrLf & _
           "- 4 Pivot tabele" & vbCrLf & _
           "- 2 Grafikona" & vbCrLf & vbCrLf & _
           "Slikaj svaki sheet za seminarski!", vbInformation

End Sub
