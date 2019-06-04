# Barcode Scanning with Lego Boost and Webcam

## Usage
1. Download [Dynamsoft Barcode Reader SDK for Linux](https://www.dynamsoft.com/Products/barcode-reader-c-api-linux.aspx). Copy `libDynamsoftBarcodeReader.so` to `/usr/lib`.
2. Get a [free trial license](https://www.dynamsoft.com/CustomerPortal/Portal/Triallicense.aspx) of Dynamsoft Barcode SDK.
3. Build the Python barcode library by following https://github.com/dynamsoft-dbr/python.
4. Install one of the Bluetooth backends:
    
    ```
    pip install pygatt
    pip install gatt
    pip install gattlib
    pip install bluepy
    ```
    
    I use Gatt Backend in my code.
    
5. Install [pylgbst](https://github.com/undera/pylgbst) to interact with `Lego Boost Move Hub`. 
6. Set a valid license:

    ```py
    dbr.initLicense('LICENSE-KEY')
    ```
  
7. Run the app:

    ```
    python3 app.py
    ```

    ![lego boost webcam barcode](https://www.codepool.biz/wp-content/uploads/2019/06/lego-boost-webcam-barcode.gif)

## Keys
- `a`: left
- `d`: right
- `w`: up
- `s`: down
- `q`: terminate the app
- `c`: capture images and scan barcodes

## Blog
[Making a Barcode Scan Robot with Lego Boost and Webcam](https://www.codepool.biz/barcode-scan-robot-lego-boost-webcam.html)
