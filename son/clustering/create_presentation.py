"""
RFM Müşteri Segmentasyonu Projesi - PDF Sunum Oluşturucu
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Türkçe karakter desteği için font kaydetme
# ReportLab Unicode desteği için özel font gerektirir

TURKISH_FONT = 'Helvetica'
TURKISH_FONT_BOLD = 'Helvetica-Bold'

# Windows'ta yaygın Unicode fontları kontrol et ve kaydet
font_paths = [
    ('C:/Windows/Fonts/ARIALUNI.TTF', 'ArialUni', 'ArialUni'),  # Arial Unicode MS
    ('C:/Windows/Fonts/tahoma.ttf', 'Tahoma', 'Tahoma'),        # Tahoma
    ('C:/Windows/Fonts/tahomabd.ttf', 'Tahoma', 'TahomaBold'),  # Tahoma Bold
    ('C:/Windows/Fonts/calibri.ttf', 'Calibri', 'Calibri'),     # Calibri
    ('C:/Windows/Fonts/calibrib.ttf', 'Calibri', 'CalibriBold'), # Calibri Bold
]

font_registered = False
for font_path, font_name, bold_name in font_paths:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            TURKISH_FONT = font_name
            # Bold versiyonu için ayrı dosya varsa kaydet
            bold_path = font_path.replace('.ttf', 'bd.ttf').replace('.TTF', 'BD.TTF')
            if os.path.exists(bold_path):
                try:
                    pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                    TURKISH_FONT_BOLD = bold_name
                except:
                    TURKISH_FONT_BOLD = font_name
            else:
                TURKISH_FONT_BOLD = font_name
            font_registered = True
            break
        except Exception as e:
            continue

# Eğer hiçbir font kaydedilemediyse, varsayılan fontları kullan
# Ancak Türkçe karakterler için Unicode desteği olmayacak
if not font_registered:
    # Windows'ta genellikle bulunan fontları tekrar dene
    import platform
    if platform.system() == 'Windows':
        # Arial Unicode MS genellikle Windows'ta yüklüdür
        arial_uni_path = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts', 'ARIALUNI.TTF')
        if os.path.exists(arial_uni_path):
            try:
                pdfmetrics.registerFont(TTFont('ArialUni', arial_uni_path))
                TURKISH_FONT = 'ArialUni'
                TURKISH_FONT_BOLD = 'ArialUni'
                font_registered = True
            except:
                pass

def create_presentation():
    """RFM Segmentasyon Projesi için PDF sunum oluştur"""
    
    # PDF dosya yolu
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "RFM_Musteri_Segmentasyonu_Sunum.pdf")
    
    # Font kayıt durumunu kontrol et
    print(f"Kullanilan font: {TURKISH_FONT} (Bold: {TURKISH_FONT_BOLD})")
    
    # PDF dokümanı oluştur
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Stil tanımlamaları
    styles = getSampleStyleSheet()
    
    # Özel stiller - Türkçe karakter desteği ile
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName=TURKISH_FONT_BOLD
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12,
        fontName=TURKISH_FONT_BOLD
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=10,
        spaceBefore=10,
        fontName=TURKISH_FONT_BOLD
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#212121'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14,
        fontName=TURKISH_FONT
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#212121'),
        spaceAfter=8,
        leftIndent=20,
        bulletIndent=10,
        fontName=TURKISH_FONT
    )
    
    # İçerik oluştur
    story = []
    
    # Kapak Sayfası
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("RFM Metodu ile Müşteri Segmentasyonu", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Online Retail II Veri Seti Analizi", heading_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Lifetimes Kütüphanesi ve K-means Algoritması Kullanımı", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, 
                                        alignment=TA_CENTER, textColor=colors.HexColor('#616161'))))
    story.append(PageBreak())
    
    # 1. Giriş
    story.append(Paragraph("1. Proje Özeti", heading_style))
    story.append(Paragraph(
        "Bu projede, Online Retail II veri seti kullanılarak RFM (Recency, Frequency, Monetary) "
        "metodu ile müşteri segmentasyonu gerçekleştirilmiştir. İki farklı yaklaşım kullanılmıştır:",
        normal_style))
    story.append(Paragraph("• Lifetimes kütüphanesi ile otomatik RFM hesaplama", bullet_style))
    story.append(Paragraph("• K-means algoritması ile denetimsiz öğrenme tabanlı segmentasyon", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 2. RFM Metodolojisi
    story.append(Paragraph("2. RFM Metodolojisi", heading_style))
    story.append(Paragraph(
        "RFM, müşterileri satın alma davranışlarına göre segmentlere ayırmak için kullanılan "
        "davranışsal segmentasyon yöntemidir.",
        normal_style))
    
    story.append(Paragraph("2.1. RFM Bileşenleri", subheading_style))
    
    rfm_components = [
        ["<b>Recency (Yenilik)</b>", "Müşterinin en son satın alma işleminden sonraki pasif kalma süresi"],
        ["<b>Frequency (Sıklık)</b>", "Müşterinin yaptığı tekrar satın alma sayısı"],
        ["<b>Monetary Value (Parasal Değer)</b>", "Müşterinin belirli bir zaman diliminde harcadığı ortalama para miktarı"]
    ]
    
    rfm_table = Table(rfm_components, colWidths=[2*inch, 4.5*inch])
    rfm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(rfm_table)
    story.append(Spacer(1, 0.2*inch))
    
    # 3. Veri Hazırlama
    story.append(Paragraph("3. Veri Hazırlama", heading_style))
    story.append(Paragraph(
        "Online Retail II veri seti kullanılarak analiz gerçekleştirilmiştir. "
        "Veri seti hazırlama adımları:",
        normal_style))
    story.append(Paragraph("• Veri içe aktarma ve sütun standartlaştırma", bullet_style))
    story.append(Paragraph("• Eksik değerlerin temizlenmesi", bullet_style))
    story.append(Paragraph("• United Kingdom verilerinin filtrelenmesi", bullet_style))
    story.append(Paragraph("• Negatif değerlerin kaldırılması", bullet_style))
    story.append(Paragraph("• Aykırı değer analizi ve temizleme", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 4. Lifetimes Kütüphanesi ile RFM
    story.append(Paragraph("4. Lifetimes Kütüphanesi ile RFM Hesaplama", heading_style))
    story.append(Paragraph(
        "Lifetimes kütüphanesi, işlemsel verilere dayalı RFM modeli oluşturabilen "
        "bir Python kütüphanesidir. Bu yaklaşım:",
        normal_style))
    story.append(Paragraph("• Otomatik RFM değerlerini hesaplar", bullet_style))
    story.append(Paragraph("• Hızlı ve pratik bir çözüm sunar", bullet_style))
    story.append(Paragraph("• Eksik değerlerin olmadığı veri setlerinde idealdir", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 5. K-means ile Segmentasyon
    story.append(Paragraph("5. K-means Algoritması ile Segmentasyon", heading_style))
    story.append(Paragraph(
        "K-means, denetimsiz öğrenme algoritmasıdır ve etiketlenmemiş verileri işler. "
        "Bu yaklaşımda:",
        normal_style))
    story.append(Paragraph("• Recency, Frequency ve Monetary değerleri için ayrı ayrı kümeleme yapılır", bullet_style))
    story.append(Paragraph("• Her değişken için 4 küme oluşturulur (0-3 arası)", bullet_style))
    story.append(Paragraph("• RFM skoru, üç küme değerinin toplamından oluşur (0-9 arası)", bullet_style))
    story.append(Paragraph("• Skorlara göre müşteriler etiketlenir: Bronze, Silver, Gold, Platinum, Diamond", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 6. Sonuçlar
    story.append(Paragraph("6. Segmentasyon Sonuçları", heading_style))
    story.append(Paragraph(
        "K-means algoritması kullanılarak oluşturulan segmentasyon sonuçları:",
        normal_style))
    
    # Segment dağılımı tablosu
    segment_results = [
        ["<b>Segment</b>", "<b>Müşteri Sayısı</b>", "<b>RFM Skoru</b>"],
        ["Diamond", "20", "6-9"],
        ["Platinum", "399", "4-5"],
        ["Gold", "1,585", "3"],
        ["Silver", "1,011", "2"],
        ["Bronze", "1,020", "0-1"]
    ]
    
    segment_table = Table(segment_results, colWidths=[2*inch, 2*inch, 2*inch])
    segment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8eaf6')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(segment_table)
    story.append(Spacer(1, 0.2*inch))
    
    # 7. Segment Özellikleri
    story.append(Paragraph("7. Segment Özellikleri", heading_style))
    
    segment_features = [
        ["<b>Diamond</b>", "En değerli müşteriler. Yüksek recency, frequency ve monetary değerleri."],
        ["<b>Platinum</b>", "Çok değerli müşteriler. İyi recency ve frequency, yüksek monetary değerleri."],
        ["<b>Gold</b>", "Değerli müşteriler. Orta-iyi seviyede RFM değerleri."],
        ["<b>Silver</b>", "Potansiyel müşteriler. Düşük-orta seviyede RFM değerleri."],
        ["<b>Bronze</b>", "Risk altındaki müşteriler. Düşük RFM değerleri, kayıp riski yüksek."]
    ]
    
    features_table = Table(segment_features, colWidths=[1.5*inch, 5*inch])
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(features_table)
    story.append(Spacer(1, 0.2*inch))
    
    # 8. Sonuçlar ve Öneriler
    story.append(Paragraph("8. Sonuçlar ve Öneriler", heading_style))
    
    story.append(Paragraph("8.1. RFM Segmentasyonunun Avantajları", subheading_style))
    story.append(Paragraph("• Kolay ve sezgisel bir yöntemdir", bullet_style))
    story.append(Paragraph("• Pazarlama ekibi tarafından kolayca anlaşılabilir", bullet_style))
    story.append(Paragraph("• Müşteri tabanını iyi tanımak için kullanılabilir", bullet_style))
    story.append(Paragraph("• Segmentlere göre farklı stratejiler uygulanabilir", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("8.2. RFM Segmentasyonunun Sınırlamaları", subheading_style))
    story.append(Paragraph("• Sadece üç faktörü dikkate alır (Recency, Frequency, Monetary)", bullet_style))
    story.append(Paragraph("• Demografik detaylar ve ürün türleri gibi faktörleri göz ardı eder", bullet_style))
    story.append(Paragraph("• Tarihsel verilere dayanır, gelecekteki durumu tam yansıtmayabilir", bullet_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("8.3. Yaklaşım Karşılaştırması", subheading_style))
    story.append(Paragraph(
        "<b>Lifetimes Kütüphanesi:</b> Eksik değerlerin olmadığı veri setlerinde daha hızlı, "
        "kolay ve pratiktir. Otomatik RFM hesaplama sağlar.",
        normal_style))
    story.append(Paragraph(
        "<b>K-means Algoritması:</b> Eksik değerlerin olduğu durumlarda daha esnektir. "
        "Daha fazla kontrol ve özelleştirme imkanı sunar.",
        normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 9. İş Stratejileri
    story.append(Paragraph("9. Segment Bazlı İş Stratejileri", heading_style))
    
    strategies = [
        ["<b>Diamond</b>", "VIP programları, özel indirimler, erken erişim fırsatları"],
        ["<b>Platinum</b>", "Özel kampanyalar, sadakat programları, kişiselleştirilmiş öneriler"],
        ["<b>Gold</b>", "Standart kampanyalar, e-posta pazarlama, çapraz satış fırsatları"],
        ["<b>Silver</b>", "Yeniden aktivasyon kampanyaları, teşvik programları"],
        ["<b>Bronze</b>", "Kayıp önleme kampanyaları, özel teklifler, müşteri geri kazanma"]
    ]
    
    strategies_table = Table(strategies, colWidths=[1.5*inch, 5*inch])
    strategies_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(strategies_table)
    story.append(Spacer(1, 0.2*inch))
    
    # 10. Sonuç
    story.append(Paragraph("10. Genel Değerlendirme", heading_style))
    story.append(Paragraph(
        "RFM segmentasyonu, müşteri tabanını anlamak ve segmentlere göre stratejiler geliştirmek "
        "için etkili bir yöntemdir. Ancak kararları sadece RFM segmentasyonuna göre almak yerine, "
        "diğer analiz yöntemleriyle birlikte değerlendirmek daha sağlıklı sonuçlar verecektir.",
        normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Son sayfa
    story.append(Paragraph("Teşekkürler", 
                          ParagraphStyle('Thanks', parent=styles['Normal'], fontSize=14, 
                                        alignment=TA_CENTER, textColor=colors.HexColor('#616161'))))
    
    # PDF'i oluştur
    doc.build(story)
    abs_path = os.path.abspath(output_path)
    # Print için encoding sorununu önle
    try:
        print(f"PDF sunum başarıyla oluşturuldu: {abs_path}")
    except UnicodeEncodeError:
        print(f"PDF sunum basariyla olusturuldu: {abs_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()

