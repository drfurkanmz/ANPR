# ANPR
# License Plate Detection and Character Recognition

This project aims to detect license plates in car images and recognize the characters on the license plates using ANPR.

## Description

The project uses image processing techniques to detect the license plate in an image and then identifies the characters on the plate. The steps involved are:
1. Edge detection and morphological operations to find the license plate.
2. Extracting the license plate area.
3. Further processing the extracted plate to detect individual characters.
4. Comparing the detected characters with a set of templates to recognize them.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/drfurkanmz/ANPR.git
    cd ANPR
    ```

2. Install the required packages:
    ```
    You can find packages in requirements.txt
    ```

3.  Update the `dosya` path in the script to point to this directory.


    

# ANPR
# Plaka Tespiti ve Karakter Tanıma

Bu proje, araba görüntülerindeki plakaları tespit etmeyi ve plakadaki karakterleri opencv kullanarak tanımayı amaçlamaktadır.

## Usage

Proje, bir görüntüdeki plakayı tespit etmek ve ardından plakadaki karakterleri tanımlamak için görüntü işleme tekniklerini kullanır. İçerilen adımlar şunlardır:
1. Kenar tespiti ve morfolojik işlemler ile plakayı bulma.
2. Plaka alanını çıkarma.
3. Çıkarılan plakayı daha fazla işleyerek bireysel karakterleri tespit etme.
4. Tespit edilen karakterleri bir dizi şablonla karşılaştırarak tanıma.

## Kurulum

1. Depoyu klonlayın:
    ```bash
    git clone https://github.com/drfurkanmz/ANPR.git
    cd ANPR
    ```

2. Gerekli paketleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3. Gorsellerin ve Templatelerin yollarini koda uyarlamayi unutmayin!

Fonksiyonlar: 

EdgeDetectMorph(image): Giriş görüntüsünü gri tonlamaya dönüştürür, Gaussian bulanıklığı uygular ve Canny kenar tespiti ve morfolojik işlemleri kullanarak kenarları vurgular.

FindArea(image, closedimage): Kenar tespit edilmiş görüntüdeki konturları bulur ve alanı ve en-boy oranı plaka olması muhtemel konturu seçer.

Plate(image, liste): Görüntüden tespit edilen plaka bölgesini çıkarır.

PlakaMorphAndDetectPlaces(plaka): Plaka görüntüsünü daha fazla işleyerek bireysel karakter konumlarını bulur.

Words(image, konumlar): Tespit edilen konumlara göre plaka üzerindeki bireysel karakter görüntülerini çıkarır.
HarfTemplates(): Belirtilen dizinden karakter şablonlarını yükler ve karşılaştırma için işler.

ResizeCharAndCompare(harfler, temp): Tespit edilen karakterleri yeniden boyutlandırır ve tanımak için şablonlarla karşılaştırır.

ResizeCharAndCompare1(harfler, temp): ResizeCharAndCompare fonksiyonuna benzer, ancak Türkiye plakalarinin formatina biraz daha uygun karakter tanıma yöntemi kullanır.

### Conda Kullanarak Ortamın Kurulumu

1. Depoyu klonlayın:
    ```bash
    git clone https://github.com/drfurkanmz/ANPR.git
    cd ANPR
    ```

2. Yeni bir conda ortamı oluşturun ve etkinleştirin:
    ```bash
    conda create --name plaka_tespiti python=3.9
    conda activate plaka_tespiti
    ```

3. Gerekli paketleri yükleyin:
    ```bash
    conda install --file requirements.txt
    ```





