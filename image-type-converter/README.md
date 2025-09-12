# 🖼️ Advanced Image File Converter

A professional, feature-rich image conversion tool with a modern GUI built in Python. Convert between multiple image formats with advanced options like quality control, resizing, batch processing, and more.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🎯 Core Conversion Features
- **Multi-format Support**: PNG, JPEG, GIF, BMP, TIFF, WEBP, HEIC/HEIF
- **Quality Control**: Adjustable quality settings (1-100%)
- **Smart Resizing**: Maintain aspect ratio with customizable dimensions
- **Metadata Preservation**: Keep EXIF data when converting
- **Format Optimization**: Tailored settings for each output format

### 🚀 Advanced Features
- **Batch Processing**: Convert multiple files or entire folders
- **Quick Convert**: One-click conversions for common formats
- **File Preview**: Preview images before conversion
- **Progress Tracking**: Real-time progress with detailed status
- **Conversion History**: Track all conversions with timestamps
- **Stop/Cancel**: Ability to cancel ongoing conversions

### 🎨 User Interface
- **Modern GUI**: Clean, intuitive interface built with tkinter
- **Tabbed Design**: Organized features in logical sections
- **Scrollable Interface**: Works in any window size
- **Responsive Layout**: Always-visible controls and progress
- **Status Bar**: Real-time feedback and updates

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/advanced-image-converter.git
   cd advanced-image-converter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python image_converter_gui.py
   ```

### Manual Installation
If you prefer to install dependencies manually:
```bash
pip install Pillow>=11.1.0 pillow-heif>=1.1.0
```

## 🚀 Usage

### Basic Conversion
1. **Launch the application**
2. **Select files**: Click "Browse Files" or "Browse Folder"
3. **Choose formats**: Select source and destination formats
4. **Adjust quality**: Use the quality slider (1-100%)
5. **Set output directory**: Choose where to save converted files
6. **Convert**: Click "Convert Files" and watch the progress

### Advanced Features

#### Batch Processing
- **Quick Convert Buttons**: One-click conversions for common formats
  - HEIC → PNG (iPhone photos)
  - JPEG → PNG
  - PNG → JPEG
  - All → WEBP (modern web format)

#### Folder Processing
- Select entire folders for batch conversion
- Recursive processing of subdirectories
- Preserve or flatten folder structure

#### Quality & Resize Options
- **Quality Control**: Fine-tune output quality for lossy formats
- **Smart Resizing**: Automatically maintain aspect ratio
- **Custom Dimensions**: Set maximum width and height

#### Preview & History
- **File Preview**: See images before converting
- **Conversion History**: Track all your conversions
- **Export History**: Save conversion logs to files

## 📁 Project Structure

```
advanced-image-converter/
├── image_converter_gui.py    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```

## 🛠️ Technical Details

### Supported Formats
| Format | Input | Output | Notes |
|--------|-------|--------|-------|
| PNG | ✅ | ✅ | Lossless, supports transparency |
| JPEG | ✅ | ✅ | Lossy, quality adjustable |
| GIF | ✅ | ✅ | Animation support |
| BMP | ✅ | ✅ | Uncompressed bitmap |
| TIFF | ✅ | ✅ | High quality, metadata support |
| WEBP | ✅ | ✅ | Modern web format |
| HEIC/HEIF | ✅ | ✅ | iPhone photos (requires pillow-heif) |

### Dependencies
- **Pillow**: Core image processing library
- **pillow-heif**: HEIC/HEIF format support
- **tkinter**: GUI framework (included with Python)

### Performance
- **Threaded Processing**: Non-blocking UI during conversion
- **Memory Efficient**: Processes files individually
- **Progress Tracking**: Real-time updates and cancellation support

## 🎯 Use Cases

### Photography
- Convert iPhone HEIC photos to PNG/JPEG
- Batch process photo collections
- Resize images for web use
- Preserve metadata and quality

### Web Development
- Convert images to web-optimized formats
- Batch resize images for responsive design
- Optimize file sizes with quality control

### General Use
- Format conversion for compatibility
- Batch processing of image collections
- Quality optimization for storage

## 🔧 Configuration

### Settings
The application saves your preferences in `converter_settings.json`:
- Default output format
- Quality settings
- Resize preferences
- Output directory

### Customization
- Modify supported formats in the code
- Adjust default quality settings
- Customize UI layout and colors

## 🐛 Troubleshooting

### Common Issues

**HEIC files not opening**:
- Ensure `pillow-heif` is installed: `pip install pillow-heif`
- Check if HEIC files are corrupted

**Conversion fails**:
- Verify file permissions
- Check available disk space
- Ensure output directory exists

**GUI not responding**:
- Large files may take time to process
- Use the Stop button to cancel if needed
- Check system resources

### Error Messages
- **"No files selected"**: Choose files using Browse Files or Browse Folder
- **"No output directory"**: Select an output folder before converting
- **"Format not supported"**: Check if the format is in the supported list

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Bug Reports
- Use GitHub Issues to report bugs
- Include Python version and error messages
- Describe steps to reproduce the issue

### Feature Requests
- Suggest new features via GitHub Issues
- Explain the use case and benefits
- Consider implementation complexity

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pillow (PIL)**: Core image processing capabilities
- **pillow-heif**: HEIC/HEIF format support
- **tkinter**: GUI framework
- **Python Community**: For excellent documentation and support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/advanced-image-converter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/advanced-image-converter/discussions)
- **Email**: your.email@example.com

## 🔄 Changelog

### Version 2.0.0 (Current)
- Complete UI redesign with tabbed interface
- Added batch processing capabilities
- Implemented quality control and resizing
- Added conversion history and preview
- Enhanced error handling and progress tracking

### Version 1.0.0
- Basic image conversion functionality
- Simple GUI interface
- Support for common formats

---

**Made with ❤️ using Python**

*If you find this project helpful, please give it a ⭐ on GitHub!*
