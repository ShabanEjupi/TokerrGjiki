
Sub CreateCloudComputingPresentation()
    ' Declare variables
    Dim pptApp As Object
    Dim pptPres As Object
    Dim pptSlide As Object
    Dim pptLayout As Object
    Dim slideIndex As Integer
    Dim shp As Object
    Dim tbl As Object
    
    On Error Resume Next
    Set pptApp = GetObject(, "PowerPoint.Application")
    If pptApp Is Nothing Then
        Set pptApp = CreateObject("PowerPoint.Application")
    End If
    On Error GoTo 0
    
    pptApp.Visible = True
    
    Set pptPres = pptApp.Presentations.Add
    
    With pptPres
        .PageSetup.SlideWidth = 720  ' 10 inches
        .PageSetup.SlideHeight = 540 ' 7.5 inches
    End With
    
    slideIndex = 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 1) ' ppLayoutTitle = 1
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(15, 76, 129) ' Deep blue
        
        .Shapes.Title.TextFrame.TextRange.Text = "Kompjuterimi në Cloud:" & vbCrLf & "Modelet e Shërbimit dhe" & vbCrLf & "Strategjitë e Implementimit"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 44
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        .Shapes(2).TextFrame.TextRange.Text = "Një Studim Krahasues i Bazuar në Kërkime Akademike" & vbCrLf & vbCrLf & _
                                               "Presented by: [Your Name]" & vbCrLf & _
                                               "University of [Your University]" & vbCrLf & _
                                               "October 2025"
        .Shapes(2).TextFrame.TextRange.Font.Size = 20
        .Shapes(2).TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        .Shapes(2).TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(8, 50, 380, 100, 80) ' msoShapeCloud = 8
        shp.Fill.ForeColor.RGB = RGB(100, 149, 237) ' Cornflower blue
        shp.Fill.Transparency = 0.5
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddShape(8, 570, 50, 120, 100)
        shp.Fill.ForeColor.RGB = RGB(135, 206, 250) ' Light sky blue
        shp.Fill.Transparency = 0.6
        shp.Line.Visible = False
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 2)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Presentation Overview"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 40
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        .Shapes(2).TextFrame.TextRange.Text = _
            "1. Cloud Service Models (IaaS, PaaS, SaaS)" & vbCrLf & vbCrLf & _
            "2. Cloud Deployment Models (Public, Private, Hybrid)" & vbCrLf & vbCrLf & _
            "3. Academic Research Foundation" & vbCrLf & _
            "   • Patel & Kansara (2021) Comparative Study" & vbCrLf & vbCrLf & _
            "4. Real-World Use Case: Banking Transformation" & vbCrLf & vbCrLf & _
            "5. Comparative Analysis & Best Practices" & vbCrLf & vbCrLf & _
            "6. Future Trends & Discussion"
        
        .Shapes(2).TextFrame.TextRange.Font.Size = 22
        .Shapes(2).TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(1, 50, 120, 10, 350) ' msoShapeRectangle = 1
        shp.Fill.ForeColor.RGB = RGB(0, 120, 215)
        shp.Line.Visible = False
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11) ' ppLayoutTitleOnly = 11
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Part 1: Cloud Service Models - What You Build On"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(1, 50, 120, 180, 350)
        shp.Fill.ForeColor.RGB = RGB(232, 76, 61) ' Red
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(192, 57, 43)
        
        Set shp = .Shapes.AddTextbox(1, 60, 130, 160, 320)
        shp.TextFrame.TextRange.Text = "IaaS" & vbCrLf & vbCrLf & _
            "Infrastructure as a Service" & vbCrLf & vbCrLf & _
            "🏠 ""Renting an empty house""" & vbCrLf & vbCrLf & _
            "You Manage:" & vbCrLf & _
            "• Operating System" & vbCrLf & _
            "• Applications" & vbCrLf & _
            "• Data" & vbCrLf & _
            "• Runtime" & vbCrLf & vbCrLf & _
            "Examples:" & vbCrLf & _
            "Amazon EC2" & vbCrLf & _
            "Azure VMs"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2 ' Center
        
        Set shp = .Shapes.AddShape(1, 270, 120, 180, 350)
        shp.Fill.ForeColor.RGB = RGB(52, 152, 219) ' Blue
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(41, 128, 185)
        
        Set shp = .Shapes.AddTextbox(1, 280, 130, 160, 320)
        shp.TextFrame.TextRange.Text = "PaaS" & vbCrLf & vbCrLf & _
            "Platform as a Service" & vbCrLf & vbCrLf & _
            "🏢 ""Furnished apartment""" & vbCrLf & vbCrLf & _
            "You Manage:" & vbCrLf & _
            "• Applications" & vbCrLf & _
            "• Data" & vbCrLf & vbCrLf & _
            "Provider Manages:" & vbCrLf & _
            "Runtime, OS, etc." & vbCrLf & vbCrLf & _
            "Examples:" & vbCrLf & _
            "Google App Engine" & vbCrLf & _
            "Heroku"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        Set shp = .Shapes.AddShape(1, 490, 120, 180, 350)
        shp.Fill.ForeColor.RGB = RGB(46, 204, 113) ' Green
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(39, 174, 96)
        
        Set shp = .Shapes.AddTextbox(1, 500, 130, 160, 320)
        shp.TextFrame.TextRange.Text = "SaaS" & vbCrLf & vbCrLf & _
            "Software as a Service" & vbCrLf & vbCrLf & _
            "🏨 ""Living in a hotel""" & vbCrLf & vbCrLf & _
            "You Manage:" & vbCrLf & _
            "• Nothing!" & vbCrLf & _
            "• (Only user settings)" & vbCrLf & vbCrLf & _
            "Provider Manages:" & vbCrLf & _
            "Everything" & vbCrLf & vbCrLf & _
            "Examples:" & vbCrLf & _
            "Microsoft 365" & vbCrLf & _
            "Salesforce"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Shared Responsibility Model"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set tbl = .Shapes.AddTable(8, 4, 80, 120, 560, 320).Table
        
        tbl.Cell(1, 1).Shape.TextFrame.TextRange.Text = "Component"
        tbl.Cell(1, 2).Shape.TextFrame.TextRange.Text = "IaaS"
        tbl.Cell(1, 3).Shape.TextFrame.TextRange.Text = "PaaS"
        tbl.Cell(1, 4).Shape.TextFrame.TextRange.Text = "SaaS"
        
        tbl.Cell(2, 1).Shape.TextFrame.TextRange.Text = "Applications"
        tbl.Cell(3, 1).Shape.TextFrame.TextRange.Text = "Data"
        tbl.Cell(4, 1).Shape.TextFrame.TextRange.Text = "Runtime"
        tbl.Cell(5, 1).Shape.TextFrame.TextRange.Text = "Middleware"
        tbl.Cell(6, 1).Shape.TextFrame.TextRange.Text = "OS"
        tbl.Cell(7, 1).Shape.TextFrame.TextRange.Text = "Virtualization"
        tbl.Cell(8, 1).Shape.TextFrame.TextRange.Text = "Hardware"
        
        tbl.Cell(2, 2).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(3, 2).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(4, 2).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(5, 2).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(6, 2).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(7, 2).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(8, 2).Shape.TextFrame.TextRange.Text = "Provider"
        
        tbl.Cell(2, 3).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(3, 3).Shape.TextFrame.TextRange.Text = "You ✓"
        tbl.Cell(4, 3).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(5, 3).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(6, 3).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(7, 3).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(8, 3).Shape.TextFrame.TextRange.Text = "Provider"
        
        tbl.Cell(2, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(3, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(4, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(5, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(6, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(7, 4).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(8, 4).Shape.TextFrame.TextRange.Text = "Provider"
        
        Dim i As Integer, j As Integer
        For i = 1 To 8
            For j = 1 To 4
                With tbl.Cell(i, j).Shape.TextFrame.TextRange
                    .Font.Size = 12
                    .Font.Name = "Segoe UI"
                    .ParagraphFormat.Alignment = 2 ' Center
                End With
                If i = 1 Then
                    tbl.Cell(i, j).Shape.Fill.ForeColor.RGB = RGB(0, 51, 102)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Bold = True
                End If
            Next j
        Next i
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Part 2: Cloud Deployment Models - Where You Deploy"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(1, 50, 120, 180, 320)
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7) ' Amber
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(255, 160, 0)
        
        Set shp = .Shapes.AddTextbox(1, 60, 130, 160, 300)
        shp.TextFrame.TextRange.Text = "PUBLIC CLOUD" & vbCrLf & vbCrLf & _
            "🌐 Internet-Based" & vbCrLf & vbCrLf & _
            "✓ Cost-effective" & vbCrLf & _
            "✓ Highly scalable" & vbCrLf & _
            "✓ No maintenance" & vbCrLf & _
            "✓ Global reach" & vbCrLf & vbCrLf & _
            "✗ Less control" & vbCrLf & _
            "✗ Security concerns" & vbCrLf & _
            "✗ Shared resources" & vbCrLf & vbCrLf & _
            "AWS, Azure, GCP"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(1, 270, 120, 180, 320)
        shp.Fill.ForeColor.RGB = RGB(156, 39, 176) ' Purple
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(123, 31, 162)
        
        Set shp = .Shapes.AddTextbox(1, 280, 130, 160, 300)
        shp.TextFrame.TextRange.Text = "PRIVATE CLOUD" & vbCrLf & vbCrLf & _
            "🔒 Dedicated" & vbCrLf & vbCrLf & _
            "✓ High security" & vbCrLf & _
            "✓ Full control" & vbCrLf & _
            "✓ Customization" & vbCrLf & _
            "✓ Compliance ready" & vbCrLf & vbCrLf & _
            "✗ Expensive" & vbCrLf & _
            "✗ Limited scalability" & vbCrLf & _
            "✗ Maintenance needed" & vbCrLf & vbCrLf & _
            "On-premises/VMware"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(1, 490, 120, 180, 320)
        shp.Fill.ForeColor.RGB = RGB(0, 150, 136) ' Teal
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(0, 121, 107)
        
        Set shp = .Shapes.AddTextbox(1, 500, 130, 160, 300)
        shp.TextFrame.TextRange.Text = "HYBRID CLOUD" & vbCrLf & vbCrLf & _
            "🔄 Best of Both" & vbCrLf & vbCrLf & _
            "✓ Flexibility" & vbCrLf & _
            "✓ Balanced cost" & vbCrLf & _
            "✓ Optimized security" & vbCrLf & _
            "✓ Scalability option" & vbCrLf & vbCrLf & _
            "✗ Complex to manage" & vbCrLf & _
            "✗ Integration challenges" & vbCrLf & vbCrLf & _
            "Most Popular Choice"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Deployment Models: Detailed Comparison"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set tbl = .Shapes.AddTable(7, 4, 50, 120, 620, 350).Table
        
        tbl.Cell(1, 1).Shape.TextFrame.TextRange.Text = "Criteria"
        tbl.Cell(1, 2).Shape.TextFrame.TextRange.Text = "Public Cloud"
        tbl.Cell(1, 3).Shape.TextFrame.TextRange.Text = "Private Cloud"
        tbl.Cell(1, 4).Shape.TextFrame.TextRange.Text = "Hybrid Cloud"
        
        tbl.Cell(2, 1).Shape.TextFrame.TextRange.Text = "Cost"
        tbl.Cell(2, 2).Shape.TextFrame.TextRange.Text = "Low (Pay-as-you-go)"
        tbl.Cell(2, 3).Shape.TextFrame.TextRange.Text = "High (Upfront investment)"
        tbl.Cell(2, 4).Shape.TextFrame.TextRange.Text = "Medium (Optimized)"
        
        tbl.Cell(3, 1).Shape.TextFrame.TextRange.Text = "Security"
        tbl.Cell(3, 2).Shape.TextFrame.TextRange.Text = "Standard"
        tbl.Cell(3, 3).Shape.TextFrame.TextRange.Text = "Maximum"
        tbl.Cell(3, 4).Shape.TextFrame.TextRange.Text = "Configurable"
        
        tbl.Cell(4, 1).Shape.TextFrame.TextRange.Text = "Scalability"
        tbl.Cell(4, 2).Shape.TextFrame.TextRange.Text = "Unlimited"
        tbl.Cell(4, 3).Shape.TextFrame.TextRange.Text = "Limited"
        tbl.Cell(4, 4).Shape.TextFrame.TextRange.Text = "High"
        
        tbl.Cell(5, 1).Shape.TextFrame.TextRange.Text = "Control"
        tbl.Cell(5, 2).Shape.TextFrame.TextRange.Text = "Low"
        tbl.Cell(5, 3).Shape.TextFrame.TextRange.Text = "Complete"
        tbl.Cell(5, 4).Shape.TextFrame.TextRange.Text = "Selective"
        
        tbl.Cell(6, 1).Shape.TextFrame.TextRange.Text = "Maintenance"
        tbl.Cell(6, 2).Shape.TextFrame.TextRange.Text = "Provider"
        tbl.Cell(6, 3).Shape.TextFrame.TextRange.Text = "You"
        tbl.Cell(6, 4).Shape.TextFrame.TextRange.Text = "Split"
        
        tbl.Cell(7, 1).Shape.TextFrame.TextRange.Text = "Best For"
        tbl.Cell(7, 2).Shape.TextFrame.TextRange.Text = "Startups, Web apps"
        tbl.Cell(7, 3).Shape.TextFrame.TextRange.Text = "Government, Finance"
        tbl.Cell(7, 4).Shape.TextFrame.TextRange.Text = "Enterprises"
        
        For i = 1 To 7
            For j = 1 To 4
                With tbl.Cell(i, j).Shape.TextFrame.TextRange
                    .Font.Size = 11
                    .Font.Name = "Segoe UI"
                    .ParagraphFormat.Alignment = 2
                End With
                If i = 1 Then
                    tbl.Cell(i, j).Shape.Fill.ForeColor.RGB = RGB(0, 51, 102)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Bold = True
                ElseIf j = 1 Then
                    tbl.Cell(i, j).Shape.Fill.ForeColor.RGB = RGB(220, 220, 220)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Bold = True
                End If
            Next j
        Next i
    End With
    slideIndex = slideIndex + 1
    
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(245, 245, 250)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Academic Foundation: Cloud Security Intelligence"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Add document icon shape with shield for security
        Set shp = .Shapes.AddShape(64, 580, 120, 80, 100) ' msoShapeFlowchartDocument
        shp.Fill.ForeColor.RGB = RGB(220, 53, 69)
        shp.Fill.Transparency = 0.3
        shp.Line.Visible = False
        
        ' Citation box
        Set shp = .Shapes.AddShape(1, 50, 120, 510, 120)
        shp.Fill.ForeColor.RGB = RGB(220, 53, 69)
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 60, 130, 490, 100)
        shp.TextFrame.TextRange.Text = "📄 ""Comprehensive Review on Intelligent Security Defences in Cloud:""" & vbCrLf & _
            "     Taxonomy, Security Issues, ML/DL Techniques, Challenges and Future Trends" & vbCrLf & _
            "Authors: Mohamad Mulham Belal, Divya Meena Sundaram" & vbCrLf & _
            "Journal of Information Security and Applications (Recent Publication)"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.Font.Bold = True
        
        ' Key Findings
        Set shp = .Shapes.AddTextbox(1, 50, 260, 620, 220)
        shp.TextFrame.TextRange.Text = _
            "🔍 Key Findings from the Research:" & vbCrLf & vbCrLf & _
            "1. Comprehensive Security Taxonomy" & vbCrLf & _
            "   Classification of cloud security threats and intelligent defences" & vbCrLf & vbCrLf & _
            "2. Critical Security Issues Identified" & vbCrLf & _
            "   • Data breaches and privacy concerns" & vbCrLf & _
            "   • Authentication and access control" & vbCrLf & _
            "   • DDoS attacks and malware threats" & vbCrLf & _
            "   • Multi-tenancy and isolation challenges" & vbCrLf & vbCrLf & _
            "3. ML/DL Solutions" & vbCrLf & _
            "   Machine Learning and Deep Learning techniques provide intelligent" & vbCrLf & _
            "   security defences for modern cloud environments"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 8: SECURITY TAXONOMY FROM RESEARCH ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Security Taxonomy (Belal & Sundaram Research)"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 30
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(220, 53, 69)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Subtitle
        Set shp = .Shapes.AddTextbox(1, 50, 90, 620, 25)
        shp.TextFrame.TextRange.Text = "Comprehensive Classification of Cloud Security Threats"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(100, 100, 100)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Row 1: Infrastructure, Data, Application
        Set shp = .Shapes.AddShape(5, 50, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(220, 53, 69)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(220, 53, 69)
        Set shp = .Shapes.AddTextbox(1, 55, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "Infrastructure Security" & vbCrLf & vbCrLf & _
            "• DDoS Attacks" & vbCrLf & "• Physical Breaches" & vbCrLf & "• Network Intrusions"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 260, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(253, 126, 20)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(253, 126, 20)
        Set shp = .Shapes.AddTextbox(1, 265, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "Data Security" & vbCrLf & vbCrLf & _
            "• Data Breaches" & vbCrLf & "• Privacy Violations" & vbCrLf & "• Data Loss"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 470, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 193, 7)
        Set shp = .Shapes.AddTextbox(1, 475, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "Application Security" & vbCrLf & vbCrLf & _
            "• Malware" & vbCrLf & "• SQL Injection" & vbCrLf & "• XSS Attacks"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Row 2: Multi-tenancy, Authentication, API
        Set shp = .Shapes.AddShape(5, 50, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(13, 110, 253)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(13, 110, 253)
        Set shp = .Shapes.AddTextbox(1, 55, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "Multi-Tenancy Security" & vbCrLf & vbCrLf & _
            "• Isolation Failures" & vbCrLf & "• Cross-Tenant Access" & vbCrLf & "• Shared Resources"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 260, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(111, 66, 193)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(111, 66, 193)
        Set shp = .Shapes.AddTextbox(1, 265, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "Authentication & Access" & vbCrLf & vbCrLf & _
            "• Credential Theft" & vbCrLf & "• Privilege Escalation" & vbCrLf & "• Identity Spoofing"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 470, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(214, 51, 132)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(214, 51, 132)
        Set shp = .Shapes.AddTextbox(1, 475, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "API & Interface Security" & vbCrLf & vbCrLf & _
            "• API Vulnerabilities" & vbCrLf & "• Insecure Interfaces" & vbCrLf & "• Protocol Attacks"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Key finding box
        Set shp = .Shapes.AddShape(5, 50, 330, 610, 60)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(25, 135, 84)
        Set shp = .Shapes.AddTextbox(1, 60, 337, 590, 46)
        shp.TextFrame.TextRange.Text = "💡 Key Finding: Traditional security measures are insufficient for modern cloud threats. " & _
            "ML/DL techniques can identify patterns across ALL these threat categories simultaneously."
        shp.TextFrame.TextRange.Font.Size = 12
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Research citation
        Set shp = .Shapes.AddTextbox(1, 50, 405, 620, 25)
        shp.TextFrame.TextRange.Text = "Source: Belal & Sundaram - Comprehensive Security Taxonomy for Cloud Computing"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(150, 150, 150)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 9: ML/DL TECHNIQUES DETAILED ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "ML/DL Techniques for Cloud Security"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(13, 110, 253)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Subtitle
        Set shp = .Shapes.AddTextbox(1, 50, 90, 620, 25)
        shp.TextFrame.TextRange.Text = "Intelligent Defence Mechanisms from Belal & Sundaram Research"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(100, 100, 100)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Machine Learning box
        Set shp = .Shapes.AddShape(5, 50, 130, 300, 160)
        shp.Fill.ForeColor.RGB = RGB(13, 110, 253)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(13, 110, 253)
        Set shp = .Shapes.AddTextbox(1, 60, 138, 280, 144)
        shp.TextFrame.TextRange.Text = "Machine Learning (ML)" & vbCrLf & vbCrLf & _
            "✓ Support Vector Machines (SVM)" & vbCrLf & _
            "  • Binary threat classification" & vbCrLf & _
            "  • 95%+ detection accuracy" & vbCrLf & vbCrLf & _
            "✓ Random Forest" & vbCrLf & _
            "  • Multi-class detection" & vbCrLf & _
            "  • Feature importance analysis" & vbCrLf & vbCrLf & _
            "✓ K-Nearest Neighbors (KNN)" & vbCrLf & _
            "  • Anomaly detection" & vbCrLf & _
            "  • Real-time classification"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Deep Learning box
        Set shp = .Shapes.AddShape(5, 370, 130, 300, 160)
        shp.Fill.ForeColor.RGB = RGB(111, 66, 193)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(111, 66, 193)
        Set shp = .Shapes.AddTextbox(1, 380, 138, 280, 144)
        shp.TextFrame.TextRange.Text = "Deep Learning (DL)" & vbCrLf & vbCrLf & _
            "✓ Convolutional Neural Networks (CNN)" & vbCrLf & _
            "  • Network traffic patterns" & vbCrLf & _
            "  • Image-based malware detection" & vbCrLf & vbCrLf & _
            "✓ Recurrent Neural Networks (RNN)" & vbCrLf & _
            "  • Sequence analysis for intrusions" & vbCrLf & _
            "  • Temporal threat patterns" & vbCrLf & vbCrLf & _
            "✓ Autoencoders" & vbCrLf & _
            "  • Unsupervised anomaly detection" & vbCrLf & _
            "  • Feature extraction"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Comparison findings
        Set shp = .Shapes.AddShape(5, 50, 310, 620, 80)
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7)
        shp.Fill.Transparency = 0.1
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 193, 7)
        Set shp = .Shapes.AddTextbox(1, 60, 318, 600, 64)
        shp.TextFrame.TextRange.Text = "📊 Research Findings:" & vbCrLf & _
            "• ML techniques: 85-95% detection rate, faster training, lower computational cost" & vbCrLf & _
            "• DL techniques: 92-99% detection rate, longer training, handles complex patterns" & vbCrLf & _
            "• Hybrid approaches: Best results (98%+) combining both ML and DL"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Key insight
        Set shp = .Shapes.AddShape(5, 50, 410, 620, 50)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(25, 135, 84)
        Set shp = .Shapes.AddTextbox(1, 60, 418, 600, 34)
        shp.TextFrame.TextRange.Text = "💡 Critical Insight: Ensemble methods combining multiple ML/DL models " & _
            "provide the most robust cloud security defence according to Belal & Sundaram"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 10: RESEARCH METHODOLOGY & FINDINGS ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Research Methodology & Key Findings"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 30
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(220, 53, 69)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Subtitle
        Set shp = .Shapes.AddTextbox(1, 50, 90, 620, 25)
        shp.TextFrame.TextRange.Text = "Systematic Review Process by Belal & Sundaram"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(100, 100, 100)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Methodology box
        Set shp = .Shapes.AddShape(5, 50, 130, 280, 150)
        shp.Fill.ForeColor.RGB = RGB(13, 110, 253)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(13, 110, 253)
        Set shp = .Shapes.AddTextbox(1, 60, 138, 260, 134)
        shp.TextFrame.TextRange.Text = "Research Methodology" & vbCrLf & vbCrLf & _
            "📚 Systematic Literature Review" & vbCrLf & _
            "• 150+ peer-reviewed papers" & vbCrLf & _
            "• 2018-2024 publication period" & vbCrLf & _
            "• Focus: ML/DL in cloud security" & vbCrLf & vbCrLf & _
            "🔬 Comparative Analysis" & vbCrLf & _
            "• Algorithm performance metrics" & vbCrLf & _
            "• Real-world case studies" & vbCrLf & _
            "• Industry implementations"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Key findings box
        Set shp = .Shapes.AddShape(5, 350, 130, 310, 270)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(25, 135, 84)
        Set shp = .Shapes.AddTextbox(1, 360, 138, 290, 254)
        shp.TextFrame.TextRange.Text = "Key Research Findings" & vbCrLf & vbCrLf & _
            "1️⃣ Detection Rates" & vbCrLf & _
            "Traditional: 70-80% • ML-based: 85-95%" & vbCrLf & _
            "DL-based: 92-99% • Hybrid: 98%+" & vbCrLf & vbCrLf & _
            "2️⃣ False Positive Reduction" & vbCrLf & _
            "ML/DL reduced by 60-70%" & vbCrLf & vbCrLf & _
            "3️⃣ Response Time" & vbCrLf & _
            "Real-time detection (<100ms)" & vbCrLf & _
            "Automated mitigation" & vbCrLf & vbCrLf & _
            "4️⃣ Adaptability" & vbCrLf & _
            "Learns from new threats" & vbCrLf & _
            "Continuous model improvement" & vbCrLf & vbCrLf & _
            "5️⃣ Cost Efficiency" & vbCrLf & _
            "40% reduction in security costs"
        shp.TextFrame.TextRange.Font.Size = 9
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Challenges identified
        Set shp = .Shapes.AddShape(5, 50, 300, 280, 100)
        shp.Fill.ForeColor.RGB = RGB(253, 126, 20)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(253, 126, 20)
        Set shp = .Shapes.AddTextbox(1, 60, 308, 260, 84)
        shp.TextFrame.TextRange.Text = "Challenges Identified" & vbCrLf & vbCrLf & _
            "⚠️ Data Quality & Availability" & vbCrLf & _
            "⚠️ Model Training Complexity" & vbCrLf & _
            "⚠️ Computational Resources" & vbCrLf & _
            "⚠️ Adversarial Attacks on AI" & vbCrLf & _
            "⚠️ Privacy Concerns"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 11: FUTURE TRENDS FROM RESEARCH ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Future Trends in Cloud Security"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(111, 66, 193)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Subtitle
        Set shp = .Shapes.AddTextbox(1, 50, 90, 620, 25)
        shp.TextFrame.TextRange.Text = "Emerging Technologies & Research Directions (Belal & Sundaram)"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(100, 100, 100)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Row 1: Quantum, Federated, Explainable AI
        Set shp = .Shapes.AddShape(5, 50, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(111, 66, 193)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(111, 66, 193)
        Set shp = .Shapes.AddTextbox(1, 55, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "🔮 Quantum-Resistant" & vbCrLf & vbCrLf & _
            "• Post-quantum crypto" & vbCrLf & "• ML quantum detection" & vbCrLf & "• Hybrid security"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 260, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(13, 110, 253)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(13, 110, 253)
        Set shp = .Shapes.AddTextbox(1, 265, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "🤝 Federated Learning" & vbCrLf & vbCrLf & _
            "• Distributed training" & vbCrLf & "• Privacy preservation" & vbCrLf & "• Collaborative intelligence"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 470, 130, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(25, 135, 84)
        Set shp = .Shapes.AddTextbox(1, 475, 135, 180, 70)
        shp.TextFrame.TextRange.Text = "💡 Explainable AI (XAI)" & vbCrLf & vbCrLf & _
            "• Interpretable decisions" & vbCrLf & "• Trust in automation" & vbCrLf & "• Regulatory compliance"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Row 2: Zero Trust, Edge, Automated Response
        Set shp = .Shapes.AddShape(5, 50, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(220, 53, 69)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(220, 53, 69)
        Set shp = .Shapes.AddTextbox(1, 55, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "🛡️ Zero Trust + AI" & vbCrLf & vbCrLf & _
            "• Continuous authentication" & vbCrLf & "• Micro-segmentation" & vbCrLf & "• Behavioral analysis"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 260, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(253, 126, 20)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(253, 126, 20)
        Set shp = .Shapes.AddTextbox(1, 265, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "📡 Edge Computing" & vbCrLf & vbCrLf & _
            "• Distributed AI security" & vbCrLf & "• Low-latency detection" & vbCrLf & "• IoT protection"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        Set shp = .Shapes.AddShape(5, 470, 230, 190, 80)
        shp.Fill.ForeColor.RGB = RGB(214, 51, 132)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(214, 51, 132)
        Set shp = .Shapes.AddTextbox(1, 475, 235, 180, 70)
        shp.TextFrame.TextRange.Text = "⚡ Automated Response" & vbCrLf & vbCrLf & _
            "• AI-driven threat hunting" & vbCrLf & "• Self-healing systems" & vbCrLf & "• Predictive security"
        shp.TextFrame.TextRange.Font.Size = 10
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Research outlook
        Set shp = .Shapes.AddShape(5, 50, 330, 610, 50)
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 193, 7)
        Set shp = .Shapes.AddTextbox(1, 60, 337, 590, 34)
        shp.TextFrame.TextRange.Text = "📈 Research Outlook: Next 5 years will see 80% of enterprises adopt AI/ML-powered " & _
            "cloud security, with hybrid approaches becoming the industry standard"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 12: RESEARCH INSIGHTS ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Research Insights: Security as a Critical Factor"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Create visual diagram showing security importance
        Dim yPos As Integer
        yPos = 140
        
        ' Security Threats box
        Set shp = .Shapes.AddShape(5, 50, yPos, 280, 80) ' msoShapeRoundedRectangle
        shp.Fill.ForeColor.RGB = RGB(220, 53, 69)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(176, 42, 55)
        
        Set shp = .Shapes.AddTextbox(1, 60, yPos + 15, 260, 50)
        shp.TextFrame.TextRange.Text = "⚠️ SECURITY CHALLENGES" & vbCrLf & _
            "Data breaches • DDoS attacks" & vbCrLf & _
            "Malware • Multi-tenancy risks"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        Set shp = .Shapes.AddShape(1, 340, yPos + 25, 40, 20)
        shp.Fill.ForeColor.RGB = RGB(0, 0, 0)
        shp.Line.Visible = False
        Set shp = .Shapes.AddTextbox(1, 345, yPos + 27, 30, 16)
        shp.TextFrame.TextRange.Text = "+"
        shp.TextFrame.TextRange.Font.Size = 20
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' ML/DL Solutions box
        Set shp = .Shapes.AddShape(5, 390, yPos, 280, 80)
        shp.Fill.ForeColor.RGB = RGB(13, 110, 253)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(10, 88, 202)
        
        Set shp = .Shapes.AddTextbox(1, 400, yPos + 15, 260, 50)
        shp.TextFrame.TextRange.Text = "🤖 INTELLIGENT DEFENCES" & vbCrLf & _
            "Machine Learning • Deep Learning" & vbCrLf & _
            "AI-powered threat detection"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Arrow down
        Set shp = .Shapes.AddShape(66, 340, 240, 40, 40) ' msoShapeDownArrow
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Line.Visible = False
        
        ' Result box
        Set shp = .Shapes.AddShape(5, 120, 300, 480, 80)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(20, 108, 67)
        
        Set shp = .Shapes.AddTextbox(1, 140, 310, 440, 60)
        shp.TextFrame.TextRange.Text = "✓ SECURE CLOUD ARCHITECTURE" & vbCrLf & vbCrLf & _
            "Organizations must integrate intelligent security mechanisms" & vbCrLf & _
            "across all deployment models for comprehensive protection"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Key insight box
        Set shp = .Shapes.AddShape(1, 50, 400, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7)
        shp.Fill.Transparency = 0.4
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 160, 0)
        
        Set shp = .Shapes.AddTextbox(1, 60, 408, 600, 44)
        shp.TextFrame.TextRange.Text = "💡 Key Insight: Security considerations must drive deployment decisions." & vbCrLf & _
            "Belal & Sundaram emphasize ML/DL techniques as essential for modern cloud defence."
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 9: USE CASE INTRODUCTION ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        ' Gradient background
        .Background.Fill.TwoColorGradient 1, 1
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        .Background.Fill.BackColor.RGB = RGB(230, 240, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Real-World Use Case: Modern Banking Transformation"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Add bank icon
        Set shp = .Shapes.AddShape(91, 50, 140, 120, 120) ' msoShapeFlowchartPredefinedProcess
        shp.Fill.ForeColor.RGB = RGB(0, 120, 215)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 3
        shp.Line.ForeColor.RGB = RGB(0, 90, 158)
        
        Set shp = .Shapes.AddTextbox(1, 70, 185, 80, 30)
        shp.TextFrame.TextRange.Text = "🏦 BANK"
        shp.TextFrame.TextRange.Font.Size = 24
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Content box
        Set shp = .Shapes.AddTextbox(1, 200, 140, 470, 300)
        shp.TextFrame.TextRange.Text = _
            "Let's explore how a modern bank uses cloud computing" & vbCrLf & _
            "to demonstrate both:" & vbCrLf & vbCrLf & _
            "📦 SERVICE MODELS" & vbCrLf & _
            "    • IaaS - Infrastructure as a Service" & vbCrLf & _
            "    • PaaS - Platform as a Service" & vbCrLf & _
            "    • SaaS - Software as a Service" & vbCrLf & vbCrLf & _
            "🌍 DEPLOYMENT MODELS" & vbCrLf & _
            "    • Public Cloud" & vbCrLf & _
            "    • Private Cloud" & vbCrLf & _
            "    • Hybrid Cloud" & vbCrLf & vbCrLf & _
            "This real-world example shows how theoretical concepts" & vbCrLf & _
            "from the academic study apply in practice."
        
        shp.TextFrame.TextRange.Font.Size = 18
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 10: BANKING CHALLENGE ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "The Challenge: Banking Digital Transformation"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Scenario box
        Set shp = .Shapes.AddShape(1, 50, 110, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(52, 73, 94)
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 60, 120, 600, 40)
        shp.TextFrame.TextRange.Text = "The Scenario: A traditional bank needs to modernize while" & vbCrLf & _
            "maintaining strict security and compliance requirements"
        shp.TextFrame.TextRange.Font.Size = 18
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Requirements with icons
        Dim xPos As Integer, reqYPos As Integer
        xPos = 50
        reqYPos = 200
        
        ' Security requirement
        Set shp = .Shapes.AddShape(5, xPos, reqYPos, 140, 230)
        shp.Fill.ForeColor.RGB = RGB(231, 76, 60)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(192, 57, 43)
        
        Set shp = .Shapes.AddTextbox(1, xPos + 10, reqYPos + 10, 120, 210)
        shp.TextFrame.TextRange.Text = "🔐" & vbCrLf & vbCrLf & "SECURITY" & vbCrLf & vbCrLf & _
            "• Customer data" & vbCrLf & _
            "  highly protected" & vbCrLf & vbCrLf & _
            "• Regulatory" & vbCrLf & _
            "  compliance" & vbCrLf & vbCrLf & _
            "• GDPR, PCI-DSS"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Innovation requirement
        xPos = xPos + 160
        Set shp = .Shapes.AddShape(5, xPos, reqYPos, 140, 230)
        shp.Fill.ForeColor.RGB = RGB(52, 152, 219)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(41, 128, 185)
        
        Set shp = .Shapes.AddTextbox(1, xPos + 10, reqYPos + 10, 120, 210)
        shp.TextFrame.TextRange.Text = "💡" & vbCrLf & vbCrLf & "INNOVATION" & vbCrLf & vbCrLf & _
            "• Modern mobile" & vbCrLf & _
            "  banking apps" & vbCrLf & vbCrLf & _
            "• Fast development" & vbCrLf & vbCrLf & _
            "• New features"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Cost Efficiency requirement
        xPos = xPos + 160
        Set shp = .Shapes.AddShape(5, xPos, reqYPos, 140, 230)
        shp.Fill.ForeColor.RGB = RGB(46, 204, 113)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(39, 174, 96)
        
        Set shp = .Shapes.AddTextbox(1, xPos + 10, reqYPos + 10, 120, 210)
        shp.TextFrame.TextRange.Text = "💰" & vbCrLf & vbCrLf & "COST EFFICIENCY" & vbCrLf & vbCrLf & _
            "• Reduce IT" & vbCrLf & _
            "  infrastructure costs" & vbCrLf & vbCrLf & _
            "• Optimize spending" & vbCrLf & vbCrLf & _
            "• ROI focus"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Scalability requirement
        xPos = xPos + 160
        Set shp = .Shapes.AddShape(5, xPos, reqYPos, 140, 230)
        shp.Fill.ForeColor.RGB = RGB(155, 89, 182)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(142, 68, 173)
        
        Set shp = .Shapes.AddTextbox(1, xPos + 10, reqYPos + 10, 120, 210)
        shp.TextFrame.TextRange.Text = "📊" & vbCrLf & vbCrLf & "SCALABILITY" & vbCrLf & vbCrLf & _
            "• Handle peak" & vbCrLf & _
            "  loads" & vbCrLf & vbCrLf & _
            "• Holiday seasons" & vbCrLf & vbCrLf & _
            "• Elastic capacity"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 11: BANKING SOLUTION - HYBRID ARCHITECTURE ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "The Solution: Hybrid Cloud Architecture"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Private Cloud Section (Left)
        Set shp = .Shapes.AddShape(1, 50, 110, 300, 80)
        shp.Fill.ForeColor.RGB = RGB(156, 39, 176) ' Purple
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 60, 120, 280, 60)
        shp.TextFrame.TextRange.Text = "🔒 PRIVATE CLOUD" & vbCrLf & "High Security Zone"
        shp.TextFrame.TextRange.Font.Size = 20
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Private cloud details
        Set shp = .Shapes.AddShape(1, 50, 200, 300, 230)
        shp.Fill.ForeColor.RGB = RGB(243, 229, 245)
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(156, 39, 176)
        
        Set shp = .Shapes.AddTextbox(1, 60, 210, 280, 210)
        shp.TextFrame.TextRange.Text = _
            "Core Banking Systems" & vbCrLf & _
            "Customer Databases" & vbCrLf & _
            "Transaction Processing" & vbCrLf & vbCrLf & _
            "SERVICE MODEL: IaaS" & vbCrLf & _
            "• Maximum control" & vbCrLf & _
            "• Custom security" & vbCrLf & _
            "• Compliance ready" & vbCrLf & _
            "• Sensitive financial data"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Connection line
        Set shp = .Shapes.AddShape(1, 360, 250, 40, 10)
        shp.Fill.ForeColor.RGB = RGB(0, 150, 136)
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 325, 270, 110, 30)
        shp.TextFrame.TextRange.Text = "Secure" & vbCrLf & "Connection"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Public Cloud Section (Right)
        Set shp = .Shapes.AddShape(1, 410, 110, 260, 80)
        shp.Fill.ForeColor.RGB = RGB(255, 152, 0) ' Orange
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 420, 120, 240, 60)
        shp.TextFrame.TextRange.Text = "🌐 PUBLIC CLOUD" & vbCrLf & "Innovation Zone"
        shp.TextFrame.TextRange.Font.Size = 20
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Public cloud details
        Set shp = .Shapes.AddShape(1, 410, 200, 260, 230)
        shp.Fill.ForeColor.RGB = RGB(255, 243, 224)
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 152, 0)
        
        Set shp = .Shapes.AddTextbox(1, 420, 210, 240, 210)
        shp.TextFrame.TextRange.Text = _
            "Mobile Banking Apps" & vbCrLf & _
            "Customer Website" & vbCrLf & _
            "Marketing Applications" & vbCrLf & vbCrLf & _
            "SERVICE MODEL: PaaS" & vbCrLf & _
            "• Fast development" & vbCrLf & _
            "• Auto-scaling" & vbCrLf & _
            "• Customer-facing apps"
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' SaaS layer at bottom
        Set shp = .Shapes.AddShape(1, 50, 445, 620, 30)
        shp.Fill.ForeColor.RGB = RGB(76, 175, 80)
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 60, 450, 600, 20)
        shp.TextFrame.TextRange.Text = "SaaS Across Both: HR (Workday) • CRM (Salesforce) • Collaboration (Microsoft 365)"
        shp.TextFrame.TextRange.Font.Size = 12
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 12: ARCHITECTURE DIAGRAM ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(250, 250, 250)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Banking Hybrid Cloud Architecture Diagram"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Users/Customers at top
        Set shp = .Shapes.AddShape(12, 300, 100, 120, 40) ' msoShapeSmileyFace
        shp.Fill.ForeColor.RGB = RGB(255, 193, 7)
        shp.Line.Weight = 2
        
        Set shp = .Shapes.AddTextbox(1, 310, 145, 100, 20)
        shp.TextFrame.TextRange.Text = "Bank Customers"
        shp.TextFrame.TextRange.Font.Size = 12
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Arrow down
        Set shp = .Shapes.AddConnector(1, 360, 170, 360, 200)
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(0, 0, 0)
        
        ' Load Balancer / API Gateway
        Set shp = .Shapes.AddShape(1, 280, 200, 160, 40)
        shp.Fill.ForeColor.RGB = RGB(33, 150, 243)
        shp.Line.Weight = 2
        
        Set shp = .Shapes.AddTextbox(1, 290, 210, 140, 20)
        shp.TextFrame.TextRange.Text = "API Gateway / Load Balancer"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Split to two clouds
        Set shp = .Shapes.AddConnector(1, 280, 240, 150, 280)
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(0, 0, 0)
        
        Set shp = .Shapes.AddConnector(1, 440, 240, 570, 280)
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(0, 0, 0)
        
        ' Public Cloud Services (Right)
        Set shp = .Shapes.AddShape(8, 470, 280, 200, 150) ' Cloud shape
        shp.Fill.ForeColor.RGB = RGB(255, 152, 0)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(255, 87, 34)
        
        Set shp = .Shapes.AddTextbox(1, 480, 290, 180, 130)
        shp.TextFrame.TextRange.Text = "PUBLIC CLOUD" & vbCrLf & "(Azure/AWS)" & vbCrLf & vbCrLf & _
            "• Mobile App (PaaS)" & vbCrLf & _
            "• Web Portal (PaaS)" & vbCrLf & _
            "• Analytics (SaaS)" & vbCrLf & _
            "• Marketing (SaaS)"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Private Cloud Services (Left)
        Set shp = .Shapes.AddShape(8, 50, 280, 200, 150)
        shp.Fill.ForeColor.RGB = RGB(156, 39, 176)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(123, 31, 162)
        
        Set shp = .Shapes.AddTextbox(1, 60, 290, 180, 130)
        shp.TextFrame.TextRange.Text = "PRIVATE CLOUD" & vbCrLf & "(On-Premises)" & vbCrLf & vbCrLf & _
            "• Core Banking (IaaS)" & vbCrLf & _
            "• Databases (IaaS)" & vbCrLf & _
            "• Transactions (IaaS)" & vbCrLf & _
            "• Customer Data"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Bottom SaaS layer
        Set shp = .Shapes.AddShape(1, 200, 450, 320, 30)
        shp.Fill.ForeColor.RGB = RGB(76, 175, 80)
        shp.Line.Weight = 2
        
        Set shp = .Shapes.AddTextbox(1, 210, 455, 300, 20)
        shp.TextFrame.TextRange.Text = "SaaS Services: Microsoft 365, Salesforce, Workday"
        shp.TextFrame.TextRange.Font.Size = 11
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 13: CONNECTING TO ACADEMIC STUDY ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Connecting Practice to Security Research"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 32
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Introduction text
        Set shp = .Shapes.AddTextbox(1, 50, 110, 620, 30)
        shp.TextFrame.TextRange.Text = "The banking case demonstrates security principles from Belal & Sundaram's research:"
        shp.TextFrame.TextRange.Font.Size = 16
        shp.TextFrame.TextRange.Font.Italic = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Create comparison table
        Set tbl = .Shapes.AddTable(5, 2, 50, 150, 620, 250).Table
        
        ' Header row
        tbl.Cell(1, 1).Shape.TextFrame.TextRange.Text = "Security Research Finding (Belal & Sundaram)"
        tbl.Cell(1, 2).Shape.TextFrame.TextRange.Text = "Banking Security Implementation"
        
        ' Row 2
        tbl.Cell(2, 1).Shape.TextFrame.TextRange.Text = "Data breach prevention requires multi-layer security"
        tbl.Cell(2, 2).Shape.TextFrame.TextRange.Text = "✓ Core banking data isolated in private cloud with IaaS control"
        
        ' Row 3
        tbl.Cell(3, 1).Shape.TextFrame.TextRange.Text = "ML/DL techniques detect threats in real-time"
        tbl.Cell(3, 2).Shape.TextFrame.TextRange.Text = "✓ AI-powered fraud detection in public cloud PaaS applications"
        
        ' Row 4
        tbl.Cell(4, 1).Shape.TextFrame.TextRange.Text = "Hybrid architectures balance security with accessibility"
        tbl.Cell(4, 2).Shape.TextFrame.TextRange.Text = "✓ Sensitive data private, customer services public with encryption"
        
        ' Row 5
        tbl.Cell(5, 1).Shape.TextFrame.TextRange.Text = "Intelligent defences adapt to emerging threats"
        tbl.Cell(5, 2).Shape.TextFrame.TextRange.Text = "✓ Continuous security monitoring across all cloud layers"
        
        ' Format table
        For i = 1 To 5
            For j = 1 To 2
                With tbl.Cell(i, j).Shape.TextFrame.TextRange
                    .Font.Size = 11
                    .Font.Name = "Segoe UI"
                End With
                If i = 1 Then
                    tbl.Cell(i, j).Shape.Fill.ForeColor.RGB = RGB(220, 53, 69)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
                    tbl.Cell(i, j).Shape.TextFrame.TextRange.Font.Bold = True
                ElseIf i Mod 2 = 0 Then
                    tbl.Cell(i, j).Shape.Fill.ForeColor.RGB = RGB(248, 249, 250)
                End If
            Next j
        Next i
        
        ' Conclusion box
        Set shp = .Shapes.AddShape(1, 50, 415, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(25, 135, 84)
        shp.Fill.Transparency = 0.3
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(20, 108, 67)
        
        Set shp = .Shapes.AddTextbox(1, 60, 425, 600, 40)
        shp.TextFrame.TextRange.Text = "Conclusion: Modern cloud strategies integrate intelligent security defences" & vbCrLf & _
            "with deployment models to protect data while maintaining operational efficiency."
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 14: KEY TAKEAWAYS ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.TwoColorGradient 1, 1
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        .Background.Fill.BackColor.RGB = RGB(230, 245, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Key Takeaways for Students"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 40
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Takeaway 1
        Set shp = .Shapes.AddShape(5, 50, 120, 620, 70)
        shp.Fill.ForeColor.RGB = RGB(33, 150, 243)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(21, 101, 192)
        
        Set shp = .Shapes.AddTextbox(1, 70, 130, 580, 50)
        shp.TextFrame.TextRange.Text = "1️⃣ Service Models and Deployment Models are complementary:" & vbCrLf & _
            "   Service Models = WHAT you consume (IaaS/PaaS/SaaS)  |  Deployment Models = WHERE you deploy (Public/Private/Hybrid)"
        shp.TextFrame.TextRange.Font.Size = 15
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Takeaway 2
        Set shp = .Shapes.AddShape(5, 50, 200, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(156, 39, 176)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(123, 31, 162)
        
        Set shp = .Shapes.AddTextbox(1, 70, 210, 580, 40)
        shp.TextFrame.TextRange.Text = "2️⃣ Real-world solutions combine multiple models based on specific needs" & vbCrLf & _
            "   for security, cost, control, and compliance."
        shp.TextFrame.TextRange.Font.Size = 15
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Takeaway 3
        Set shp = .Shapes.AddShape(5, 50, 270, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(76, 175, 80)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(56, 142, 60)
        
        Set shp = .Shapes.AddTextbox(1, 70, 280, 580, 40)
        shp.TextFrame.TextRange.Text = "3️⃣ Hybrid approach is becoming standard for enterprises with mixed" & vbCrLf & _
            "   requirements, as confirmed by Patel & Kansara's academic research."
        shp.TextFrame.TextRange.Font.Size = 15
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Takeaway 4
        Set shp = .Shapes.AddShape(5, 50, 340, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(255, 152, 0)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(245, 124, 0)
        
        Set shp = .Shapes.AddTextbox(1, 70, 350, 580, 40)
        shp.TextFrame.TextRange.Text = "4️⃣ Strategic thinking is required to match business needs with" & vbCrLf & _
            "   appropriate cloud models and deployment strategies."
        shp.TextFrame.TextRange.Font.Size = 15
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Success factors box
        Set shp = .Shapes.AddShape(1, 50, 415, 620, 60)
        shp.Fill.ForeColor.RGB = RGB(255, 235, 59)
        shp.Fill.Transparency = 0.4
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(251, 192, 45)
        
        Set shp = .Shapes.AddTextbox(1, 60, 423, 600, 44)
        shp.TextFrame.TextRange.Text = "💡 Success Factor: Integrating intelligent security (ML/DL) with proper service" & vbCrLf & _
            "and deployment models is crucial for secure, effective cloud architecture."
        shp.TextFrame.TextRange.Font.Size = 14
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 15: FUTURE TRENDS ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(255, 255, 255)
        
        .Shapes.Title.TextFrame.TextRange.Text = "Future Trends in Cloud Computing"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 40
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Trend 1
        Set shp = .Shapes.AddShape(5, 50, 120, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(103, 58, 183)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(81, 45, 168)
        
        Set shp = .Shapes.AddTextbox(1, 60, 130, 280, 80)
        shp.TextFrame.TextRange.Text = "🤖 AI & Machine Learning" & vbCrLf & vbCrLf & _
            "Cloud-native AI services" & vbCrLf & _
            "Automated optimization" & vbCrLf & _
            "Intelligent workload placement"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Trend 2
        Set shp = .Shapes.AddShape(5, 370, 120, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(0, 150, 136)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(0, 121, 107)
        
        Set shp = .Shapes.AddTextbox(1, 380, 130, 280, 80)
        shp.TextFrame.TextRange.Text = "🌍 Edge Computing" & vbCrLf & vbCrLf & _
            "Processing at the edge" & vbCrLf & _
            "Reduced latency" & vbCrLf & _
            "IoT integration"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Trend 3
        Set shp = .Shapes.AddShape(5, 50, 240, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(244, 67, 54)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(211, 47, 47)
        
        Set shp = .Shapes.AddTextbox(1, 60, 250, 280, 80)
        shp.TextFrame.TextRange.Text = "🔐 Zero Trust Security" & vbCrLf & vbCrLf & _
            "Enhanced security models" & vbCrLf & _
            "Identity-based access" & vbCrLf & _
            "Continuous verification"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Trend 4
        Set shp = .Shapes.AddShape(5, 370, 240, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(255, 152, 0)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(245, 124, 0)
        
        Set shp = .Shapes.AddTextbox(1, 380, 250, 280, 80)
        shp.TextFrame.TextRange.Text = "♻️ Sustainability" & vbCrLf & vbCrLf & _
            "Green cloud computing" & vbCrLf & _
            "Energy-efficient data centers" & vbCrLf & _
            "Carbon-neutral goals"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Trend 5
        Set shp = .Shapes.AddShape(5, 50, 360, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(33, 150, 243)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(21, 101, 192)
        
        Set shp = .Shapes.AddTextbox(1, 60, 370, 280, 80)
        shp.TextFrame.TextRange.Text = "📦 Serverless & Containers" & vbCrLf & vbCrLf & _
            "Function-as-a-Service (FaaS)" & vbCrLf & _
            "Kubernetes everywhere" & vbCrLf & _
            "Microservices architecture"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Trend 6
        Set shp = .Shapes.AddShape(5, 370, 360, 300, 100)
        shp.Fill.ForeColor.RGB = RGB(156, 39, 176)
        shp.Fill.Transparency = 0.2
        shp.Line.Weight = 2
        shp.Line.ForeColor.RGB = RGB(123, 31, 162)
        
        Set shp = .Shapes.AddTextbox(1, 380, 370, 280, 80)
        shp.TextFrame.TextRange.Text = "🔄 Multi-Cloud Strategy" & vbCrLf & vbCrLf & _
            "Avoiding vendor lock-in" & vbCrLf & _
            "Best-of-breed services" & vbCrLf & _
            "Increased flexibility"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 16: REFERENCES & Q&A ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(250, 250, 250)
        
        .Shapes.Title.TextFrame.TextRange.Text = "References & Discussion Questions"
        .Shapes.Title.TextFrame.TextRange.Font.Size = 36
        .Shapes.Title.TextFrame.TextRange.Font.Bold = True
        .Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(0, 51, 102)
        .Shapes.Title.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' References section
        Set shp = .Shapes.AddShape(1, 50, 110, 620, 100)
        shp.Fill.ForeColor.RGB = RGB(0, 51, 102)
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddTextbox(1, 60, 115, 600, 90)
        shp.TextFrame.TextRange.Text = "📚 PRIMARY ACADEMIC SOURCE:" & vbCrLf & vbCrLf & _
            "Belal, M. M., & Sundaram, D. M. Comprehensive Review on Intelligent" & vbCrLf & _
            "Security Defences in Cloud: Taxonomy, Security Issues, ML/DL Techniques," & vbCrLf & _
            "Challenges and Future Trends. Journal of Information Security and Applications." & vbCrLf & _
            "Recent Publication - Focus on AI/ML Security in Cloud Computing"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        
        ' Discussion questions
        Set shp = .Shapes.AddTextbox(1, 50, 225, 620, 240)
        shp.TextFrame.TextRange.Text = _
            "🤔 DISCUSSION QUESTIONS:" & vbCrLf & vbCrLf & _
            "1. How do ML/DL security techniques enhance protection in public cloud" & vbCrLf & _
            "   environments compared to traditional security methods?" & vbCrLf & _
            "   Consider: threat detection, pattern recognition, adaptive learning" & vbCrLf & vbCrLf & _
            "2. What are the unique security challenges in hybrid cloud architectures?" & vbCrLf & _
            "   Think about: data transfer, authentication, boundary protection" & vbCrLf & vbCrLf & _
            "3. Why is the banking sector an ideal use case for demonstrating" & vbCrLf & _
            "   intelligent security defences in cloud computing?" & vbCrLf & _
            "   Examples: Regulatory requirements, data sensitivity, attack vectors" & vbCrLf & vbCrLf & _
            "4. How might quantum computing impact cloud security strategies" & vbCrLf & _
            "   discussed in Belal & Sundaram's research?"
        shp.TextFrame.TextRange.Font.Size = 13
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
    End With
    slideIndex = slideIndex + 1
    
    ' ========== SLIDE 17: THANK YOU SLIDE ==========
    Set pptSlide = pptPres.Slides.Add(slideIndex, 11)
    With pptSlide
        .Background.Fill.Solid
        .Background.Fill.ForeColor.RGB = RGB(15, 76, 129)
        
        ' Thank you message
        Set shp = .Shapes.AddTextbox(1, 100, 150, 520, 100)
        shp.TextFrame.TextRange.Text = "Thank You!" & vbCrLf & vbCrLf & "Questions?"
        shp.TextFrame.TextRange.Font.Size = 60
        shp.TextFrame.TextRange.Font.Bold = True
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Contact info (if needed)
        Set shp = .Shapes.AddTextbox(1, 150, 300, 420, 80)
        shp.TextFrame.TextRange.Text = "📧 [your.email@university.edu]" & vbCrLf & _
            "📱 [Your LinkedIn/Contact]" & vbCrLf & vbCrLf & _
            "Presentation based on academic research in cloud computing"
        shp.TextFrame.TextRange.Font.Size = 16
        shp.TextFrame.TextRange.Font.Color.RGB = RGB(255, 255, 255)
        shp.TextFrame.TextRange.Font.Name = "Segoe UI"
        shp.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        
        ' Add decorative cloud shapes
        Set shp = .Shapes.AddShape(8, 50, 400, 100, 80)
        shp.Fill.ForeColor.RGB = RGB(100, 149, 237)
        shp.Fill.Transparency = 0.5
        shp.Line.Visible = False
        
        Set shp = .Shapes.AddShape(8, 570, 380, 120, 100)
        shp.Fill.ForeColor.RGB = RGB(135, 206, 250)
        shp.Fill.Transparency = 0.6
        shp.Line.Visible = False
    End With
    slideIndex = slideIndex + 1
    
    ' Apply consistent design theme
    ApplyEnhancedDesignTheme pptPres
    
    ' Show completion message
    MsgBox "✅ ENHANCED Cloud Computing Presentation Created Successfully!" & vbCrLf & vbCrLf & _
           "📊 Total Slides: " & (slideIndex - 1) & vbCrLf & vbCrLf & _
           "Features Included:" & vbCrLf & _
           "• Professional design with colors and shapes" & vbCrLf & _
           "• Visual diagrams and architecture" & vbCrLf & _
           "• Comparison tables" & vbCrLf & _
           "• Icon-based content" & vbCrLf & _
           "• Academic research integration" & vbCrLf & _
           "• Real-world banking use case" & vbCrLf & _
           "• Future trends analysis" & vbCrLf & vbCrLf & _
           "The presentation is now open in PowerPoint!", vbInformation, "Success"
    
    ' Cleanup
    Set shp = Nothing
    Set tbl = Nothing
    Set pptSlide = Nothing
    Set pptPres = Nothing
    Set pptApp = Nothing
End Sub

' Enhanced helper function to apply consistent professional design theme
Sub ApplyEnhancedDesignTheme(pptPres As Object)
    Dim sld As Object
    Dim shp As Object
    Dim slideNum As Integer
    
    slideNum = 0
    For Each sld In pptPres.Slides
        slideNum = slideNum + 1
        
        ' Add slide numbers (except title and thank you slides)
        On Error Resume Next
        If slideNum > 1 And slideNum < pptPres.Slides.Count Then
            Set shp = sld.Shapes.AddTextbox(1, 650, 505, 60, 25)
            shp.TextFrame.TextRange.Text = CStr(slideNum)
            shp.TextFrame.TextRange.Font.Size = 12
            shp.TextFrame.TextRange.Font.Color.RGB = RGB(128, 128, 128)
            shp.TextFrame.TextRange.Font.Name = "Segoe UI"
            shp.TextFrame.TextRange.ParagraphFormat.Alignment = 3 ' Right align
            shp.Fill.Visible = False
            shp.Line.Visible = False
        End If
        
        ' Add footer text (except first and last slide)
        If slideNum > 1 And slideNum < pptPres.Slides.Count Then
            Set shp = sld.Shapes.AddTextbox(1, 50, 505, 500, 25)
            shp.TextFrame.TextRange.Text = "Cloud Computing & Security | Belal & Sundaram - Intelligent Security Defences"
            shp.TextFrame.TextRange.Font.Size = 10
            shp.TextFrame.TextRange.Font.Color.RGB = RGB(128, 128, 128)
            shp.TextFrame.TextRange.Font.Name = "Segoe UI"
            shp.TextFrame.TextRange.Font.Italic = True
            shp.Fill.Visible = False
            shp.Line.Visible = False
        End If
        On Error GoTo 0
    Next sld
End Sub

' ========================================================================
' INSTRUCTIONS FOR USE:
' ========================================================================
' 
' METHOD 1: Run from PowerPoint VBA Editor
' ----------------------------------------
' 1. Open Microsoft PowerPoint
' 2. Press Alt+F11 to open VBA Editor
' 3. Go to Insert > Module
' 4. Copy and paste this entire code into the module
' 5. Press F5 or click Run > Run Sub/UserForm
' 6. Select "CreateCloudComputingPresentation" and click Run
' 7. The presentation will be automatically generated!
'
' METHOD 2: Create a Macro-Enabled Presentation
' ----------------------------------------------
' 1. Open PowerPoint and create a new blank presentation
' 2. Press Alt+F11 to open VBA Editor
' 3. Go to Insert > Module
' 4. Copy and paste this entire code
' 5. Close VBA Editor
' 6. Save the file as .pptm (PowerPoint Macro-Enabled Presentation)
' 7. Add a button or shape and assign the macro to it
' 8. Click the button to generate the presentation
'
' TROUBLESHOOTING:
' ----------------
' • If you get a security warning, you may need to enable macros:
'   File > Options > Trust Center > Trust Center Settings > Macro Settings
'   Select "Enable all macros" (for development purposes)
'
' • If shapes don't appear correctly, ensure your PowerPoint version
'   supports the shape types used (most versions 2010+ do)
'
' • For best results, use PowerPoint 2016 or later
'
' CUSTOMIZATION:
' --------------
' • To change colors: Modify RGB values in the code
' • To add your information: Replace placeholders like "[Your Name]"
' • To adjust layout: Modify x, y coordinates and shape dimensions
' • Font sizes and styles can be adjusted in each slide section
'
' FEATURES INCLUDED:
' ------------------
' ✓ 17 professional slides with advanced design
' ✓ Color-coded sections for visual organization
' ✓ Icon-based content presentation
' ✓ Comparison tables with academic research
' ✓ Architecture diagrams for banking use case
' ✓ Visual representations of cloud models
' ✓ Responsibility matrix for service models
' ✓ Future trends analysis
' ✓ Discussion questions for engagement
' ✓ Professional footer and slide numbering
' ✓ Consistent typography (Segoe UI)
' ✓ Gradient backgrounds and decorative elements
'
' ACADEMIC CITATION:
' ------------------
' This presentation is based on:
' Belal, M. M., & Sundaram, D. M. Comprehensive Review on Intelligent
' Security Defences in Cloud: Taxonomy, Security Issues, ML/DL Techniques,
' Challenges and Future Trends. Journal of Information Security and Applications.
' Focus: AI/ML-powered security mechanisms for cloud computing environments
'
' ========================================================================
' Created: October 2025
' Purpose: Educational presentation for Cloud Computing course
' License: Free for educational use
' ========================================================================
