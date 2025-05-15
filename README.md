# EpLinker

**EpLinker** is a simple Python tool for creating hard links of TV show episodes with automatic file renaming using the format:  
`Series Title - S01E01.mkv`

It supports automatic episode number extraction from filenames or manual numbering.

## Features

- Creates hard links instead of copying files (saves disk space)
- Automatically renames files to consistent format
- Works with or without episode numbers in filenames

## Supported Formats

`.mkv`, `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`

## Usage

1. Run the script using Python
2. Enter the required inputs:
   - Source folder with video files
   - Target folder where links should be created
   - Series title
   - Season number
   - Whether to auto-detect episode numbers or assign manually

## Example

```bash
> Enter the path to the source folder: D:\Downloads\New Show
> Enter the path to the target folder: E:\TV Shows
> Enter the series title: The Example Show
> Enter the season number: 1
> Extract episode number from filename? (Y/N): Y
