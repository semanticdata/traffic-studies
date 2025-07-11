/**
 * Data loading utilities for Traffic Studies dashboard using Observable Framework FileAttachment.
 */

import { timeParse } from "d3-time-format";

export class TrafficDataError extends Error {
    constructor(message) {
        super(message);
        this.name = "TrafficDataError";
    }
}

export class DataValidationError extends TrafficDataError {
    constructor(message, validationDetails = {}) {
        super(message);
        this.name = "DataValidationError";
        this.validationDetails = validationDetails;
    }
}

export class FileStructureError extends TrafficDataError {
    constructor(message) {
        super(message);
        this.name = "FileStructureError";
    }
}

/**
 * Parse a CSV line handling quoted values properly
 */
function parseCSVLine(line) {
    const values = [];
    let current = '';
    let inQuotes = false;
    let i = 0;

    while (i < line.length) {
        const char = line[i];

        if (char === '"') {
            if (inQuotes && line[i + 1] === '"') {
                // Escaped quote
                current += '"';
                i += 2;
            } else {
                // Toggle quote state
                inQuotes = !inQuotes;
                i++;
            }
        } else if (char === ',' && !inQuotes) {
            // End of field
            values.push(current.trim());
            current = '';
            i++;
        } else {
            current += char;
            i++;
        }
    }

    // Add the last field
    values.push(current.trim());

    return values;
}

/**
 * Detect the structure of the CSV file and return appropriate parsing parameters
 */
export function detectFileStructure(csvText) {
    try {
        // Handle different line endings properly
        const lines = csvText.split(/\r?\n/);
        const headerLines = [];

        // Read first 15 lines to get headers
        for (let i = 0; i < Math.min(15, lines.length); i++) {
            headerLines.push(lines[i]);
        }

        // Extract metadata information
        let location = null;
        let comments = null;
        let title = null;

        for (const line of headerLines) {
            // Handle CSV format (comma-separated) and other formats
            if (line.startsWith('"Location",') || line.includes('Location:')) {
                if (line.includes('Location,')) {
                    location = line.split('Location,')[1].trim().replace(/"/g, '').replace(/'/g, '').replace(/,/g, '').trim();
                } else {
                    const parts = line.trim().split('","');
                    if (parts.length > 1) {
                        location = parts[1].replace(/"/g, '').trim();
                    } else {
                        location = line.split('Location:')[1].trim().replace(/"/g, '').replace(/'/g, '').replace(/,/g, '').trim();
                    }
                }
            } else if (line.startsWith('"Comments",') || line.includes('Comments:')) {
                if (line.includes('Comments,')) {
                    comments = line.split('Comments,')[1].trim().replace(/"/g, '').replace(/,/g, '');
                } else {
                    comments = line.split('Comments:')[1].trim().replace(/"/g, '').replace(/,/g, '');
                }
            } else if (line.startsWith('"Title",') || line.includes('Title:')) {
                if (line.includes('Title,')) {
                    title = line.split('Title,')[1].trim().replace(/"/g, '').replace(/,/g, '');
                } else {
                    title = line.split('Title:')[1].trim().replace(/"/g, '').replace(/,/g, '');
                }
            }
        }

        // Find data columns
        let columnLine = null;
        let metadataRows = -1;

        for (let i = 0; i < headerLines.length; i++) {
            if (headerLines[i].includes('Date/Time')) {
                columnLine = headerLines[i];
                metadataRows = i;
                break;
            }
        }

        if (!columnLine) {
            console.log("Header lines examined:", headerLines);
            console.log("Total lines in file:", lines.length);
            console.log("Looking for Date/Time in first 15 lines:");
            for (let i = 0; i < Math.min(15, lines.length); i++) {
                console.log(`Line ${i} (${lines[i].length} chars): "${lines[i]}"`);
                if (lines[i].includes("Date/Time")) {
                    console.log(`  -> Contains Date/Time!`);
                }
            }
            throw new FileStructureError("Could not find Date/Time column in CSV file");
        }

        // Parse columns from header line using consistent CSV parsing
        const columns = parseCSVLine(columnLine);

        // Detect direction names
        let dir1Name, dir2Name;
        if (columns.join('').includes('Northbound')) {
            dir1Name = 'Northbound';
            dir2Name = 'Southbound';
        } else {
            dir1Name = 'Eastbound';
            dir2Name = 'Westbound';
        }

        // Detect speed columns - handle both single and double space formats
        const dir1SpeedCols = columns.filter(col =>
            col.includes(`MPH - ${dir1Name}`) || col.includes(`MPH  - ${dir1Name}`)
        );
        const dir2SpeedCols = columns.filter(col =>
            col.includes(`MPH - ${dir2Name}`) || col.includes(`MPH  - ${dir2Name}`)
        );

        // Detect volume columns
        let dir1VolumeCol = null;
        let dir2VolumeCol = null;

        const volumePatterns1 = [`Volume - ${dir1Name}`, dir1Name, `${dir1Name} Volume`];
        const volumePatterns2 = [`Volume - ${dir2Name}`, dir2Name, `${dir2Name} Volume`];

        for (const pattern of volumePatterns1) {
            if (columns.includes(pattern)) {
                dir1VolumeCol = pattern;
                break;
            }
        }

        for (const pattern of volumePatterns2) {
            if (columns.includes(pattern)) {
                dir2VolumeCol = pattern;
                break;
            }
        }

        // Detect classification columns
        const dir1ClassCols = [];
        const dir2ClassCols = [];

        for (let classNum = 1; classNum <= 6; classNum++) {
            const patterns1 = [
                `Class #${classNum} - ${dir1Name}`,
                `Class ${classNum} - ${dir1Name}`,
                `Class${classNum} - ${dir1Name}`,
                `Class #${classNum}-${dir1Name}`,
                `Class ${classNum}-${dir1Name}`
            ];

            const patterns2 = [
                `Class #${classNum} - ${dir2Name}`,
                `Class ${classNum} - ${dir2Name}`,
                `Class${classNum} - ${dir2Name}`,
                `Class #${classNum}-${dir2Name}`,
                `Class ${classNum}-${dir2Name}`
            ];

            // Find matching column for direction 1
            for (const pattern of patterns1) {
                const matchingCol = columns.find(col => col.includes(pattern));
                if (matchingCol) {
                    dir1ClassCols.push(matchingCol);
                    break;
                }
            }

            // Find matching column for direction 2
            for (const pattern of patterns2) {
                const matchingCol = columns.find(col => col.includes(pattern));
                if (matchingCol) {
                    dir2ClassCols.push(matchingCol);
                    break;
                }
            }
        }

        return {
            metadataRows,
            columns,
            location: location || "Unknown Location",
            comments: comments || "",
            title: title || "",
            dir1Name,
            dir2Name,
            dir1SpeedCols,
            dir2SpeedCols,
            dir1VolumeCol,
            dir2VolumeCol,
            dir1ClassCols,
            dir2ClassCols
        };

    } catch (error) {
        console.error("Error detecting file structure:", error);
        throw new FileStructureError(`Could not detect file structure: ${error.message}`);
    }
}

/**
 * Load traffic data using Observable Framework FileAttachment
 */
export async function loadTrafficData(fileAttachment, speedLimit = 30) {
    try {
        // Load CSV text to detect structure
        const csvText = await fileAttachment.text();
        console.log("CSV loaded, length:", csvText.length);

        // Early validation - check if file is too large
        if (csvText.length > 10000000) { // 10MB limit
            throw new TrafficDataError("File too large for browser processing");
        }

        // Detect file structure
        const structure = detectFileStructure(csvText);
        console.log("Structure detected:", structure);

        // Parse CSV manually with proper structure handling
        const lines = csvText.split(/\r?\n/);
        const dataLines = lines.slice(structure.metadataRows);

        // Parse the data manually
        const cleanData = [];
        if (dataLines.length > 1) {
            // Parse headers
            const headers = parseCSVLine(dataLines[0]);

            // Parse data rows
            for (let i = 1; i < dataLines.length; i++) {
                const line = dataLines[i].trim();
                if (!line) continue;

                const values = parseCSVLine(line);
                const row = {};

                headers.forEach((header, index) => {
                    row[header] = values[index] || '';
                });

                cleanData.push(row);
            }
        }

        console.log("Clean data parsed:", cleanData.length, "rows");

        // Early exit if no data
        if (cleanData.length === 0) {
            console.warn("No valid traffic data found");
            return {
                data: [],
                location: structure.location,
                structure: structure
            };
        }

        // Process data in chunks to avoid blocking
        const processedData = await processTrafficDataAsync(cleanData, structure, speedLimit);
        console.log("Data processed:", processedData.length, "rows");

        // Filter out rows with no traffic activity
        const filteredData = processedData.filter(row => {
            const hasVolume = (row[structure.dir1VolumeCol] || 0) > 0 ||
                (row[structure.dir2VolumeCol] || 0) > 0;
            const hasValidDate = row["Date/Time"] !== null;
            return hasVolume && hasValidDate;
        });

        console.log("Data filtered:", filteredData.length, "rows");

        return {
            data: filteredData,
            location: structure.location,
            structure: structure
        };

    } catch (error) {
        console.error("Error loading traffic data:", error);
        throw new TrafficDataError(`Error loading traffic data: ${error.message}`);
    }
}

/**
 * Process raw CSV data and add computed columns (async to avoid blocking)
 */
export async function processTrafficDataAsync(rawData, structure, speedLimit = 30) {
    const parseDate = timeParse("%m/%d/%Y %H:%M");
    const chunkSize = 1000; // Process in chunks to avoid blocking
    const chunks = [];

    // Split data into chunks
    for (let i = 0; i < rawData.length; i += chunkSize) {
        chunks.push(rawData.slice(i, i + chunkSize));
    }

    const processedChunks = [];

    for (const chunk of chunks) {
        const processedChunk = chunk.map(row => {
            // Parse date/time - handle the exact format from CSV
            let dateTime = null;
            let hour = null;

            try {
                if (row["Date/Time"]) {
                    dateTime = parseDate(row["Date/Time"]);
                    hour = dateTime ? dateTime.getHours() : null;
                }
            } catch (error) {
                console.warn("Could not parse date:", row["Date/Time"], error);
                dateTime = null;
                hour = null;
            }

            // Convert string values to numbers with validation
            const processedRow = { ...row };

            // Convert volume columns to numbers
            if (structure.dir1VolumeCol && row[structure.dir1VolumeCol]) {
                const val = +row[structure.dir1VolumeCol];
                processedRow[structure.dir1VolumeCol] = isNaN(val) ? 0 : val;
            }
            if (structure.dir2VolumeCol && row[structure.dir2VolumeCol]) {
                const val = +row[structure.dir2VolumeCol];
                processedRow[structure.dir2VolumeCol] = isNaN(val) ? 0 : val;
            }

            // Convert speed columns to numbers with validation
            [...(structure.dir1SpeedCols || []), ...(structure.dir2SpeedCols || [])].forEach(col => {
                if (row[col]) {
                    const val = +row[col];
                    processedRow[col] = isNaN(val) ? 0 : val;
                }
            });

            // Convert classification columns to numbers with validation
            [...(structure.dir1ClassCols || []), ...(structure.dir2ClassCols || [])].forEach(col => {
                if (row[col]) {
                    const val = +row[col];
                    processedRow[col] = isNaN(val) ? 0 : val;
                }
            });

            // Add computed columns
            processedRow["Date/Time"] = dateTime;
            processedRow.Hour = hour;

            // Safely calculate total volume
            const vol1 = processedRow[structure.dir1VolumeCol] || 0;
            const vol2 = processedRow[structure.dir2VolumeCol] || 0;
            processedRow.Total = vol1 + vol2;

            // Calculate speed compliance efficiently
            let dir1Compliant = 0;
            let dir1NonCompliant = 0;
            let dir2Compliant = 0;
            let dir2NonCompliant = 0;

            // Process direction 1 speed compliance
            if (structure.dir1SpeedCols && Array.isArray(structure.dir1SpeedCols)) {
                for (const col of structure.dir1SpeedCols) {
                    try {
                        const speedValue = extractSpeedFromColumn(col);
                        const count = processedRow[col] || 0;

                        if (speedValue <= speedLimit) {
                            dir1Compliant += count;
                        } else {
                            dir1NonCompliant += count;
                        }
                    } catch (error) {
                        console.warn("Error processing speed column:", col, error);
                    }
                }
            }

            // Process direction 2 speed compliance
            if (structure.dir2SpeedCols && Array.isArray(structure.dir2SpeedCols)) {
                for (const col of structure.dir2SpeedCols) {
                    try {
                        const speedValue = extractSpeedFromColumn(col);
                        const count = processedRow[col] || 0;

                        if (speedValue <= speedLimit) {
                            dir2Compliant += count;
                        } else {
                            dir2NonCompliant += count;
                        }
                    } catch (error) {
                        console.warn("Error processing speed column:", col, error);
                    }
                }
            }

            processedRow.Dir1_Compliant = dir1Compliant;
            processedRow.Dir1_Non_Compliant = dir1NonCompliant;
            processedRow.Dir2_Compliant = dir2Compliant;
            processedRow.Dir2_Non_Compliant = dir2NonCompliant;

            return processedRow;
        });

        processedChunks.push(processedChunk);

        // Allow other tasks to run between chunks
        await new Promise(resolve => setTimeout(resolve, 0));
    }

    return processedChunks.flat();
}

/**
 * Process raw CSV data and add computed columns (legacy sync version)
 */
export function processTrafficData(rawData, structure, speedLimit = 30) {
    // For backward compatibility, call the async version synchronously
    console.warn("Using deprecated synchronous processTrafficData. Consider using processTrafficDataAsync.");
    return processTrafficDataSync(rawData, structure, speedLimit);
}

function processTrafficDataSync(rawData, structure, speedLimit = 30) {
    const parseDate = timeParse("%m/%d/%Y %H:%M");

    return rawData.map(row => {
        // Parse date/time - handle the exact format from CSV
        let dateTime = null;
        let hour = null;

        try {
            if (row["Date/Time"]) {
                dateTime = parseDate(row["Date/Time"]);
                hour = dateTime ? dateTime.getHours() : null;
            }
        } catch (error) {
            console.warn("Could not parse date:", row["Date/Time"], error);
            dateTime = null;
            hour = null;
        }

        // Convert string values to numbers
        const processedRow = { ...row };

        // Convert volume columns to numbers
        if (structure.dir1VolumeCol && row[structure.dir1VolumeCol]) {
            processedRow[structure.dir1VolumeCol] = +row[structure.dir1VolumeCol] || 0;
        }
        if (structure.dir2VolumeCol && row[structure.dir2VolumeCol]) {
            processedRow[structure.dir2VolumeCol] = +row[structure.dir2VolumeCol] || 0;
        }

        // Convert speed columns to numbers
        [...(structure.dir1SpeedCols || []), ...(structure.dir2SpeedCols || [])].forEach(col => {
            if (row[col]) {
                processedRow[col] = +row[col] || 0;
            }
        });

        // Convert classification columns to numbers
        [...(structure.dir1ClassCols || []), ...(structure.dir2ClassCols || [])].forEach(col => {
            if (row[col]) {
                processedRow[col] = +row[col] || 0;
            }
        });

        // Add computed columns
        processedRow["Date/Time"] = dateTime;
        processedRow.Hour = hour;

        // Safely calculate total volume
        const vol1 = processedRow[structure.dir1VolumeCol] || 0;
        const vol2 = processedRow[structure.dir2VolumeCol] || 0;
        processedRow.Total = vol1 + vol2;

        // Calculate speed compliance
        let dir1Compliant = 0;
        let dir1NonCompliant = 0;
        let dir2Compliant = 0;
        let dir2NonCompliant = 0;

        // Process direction 1 speed compliance
        if (structure.dir1SpeedCols && Array.isArray(structure.dir1SpeedCols)) {
            for (const col of structure.dir1SpeedCols) {
                try {
                    const speedValue = extractSpeedFromColumn(col);
                    const count = processedRow[col] || 0;

                    if (speedValue <= speedLimit) {
                        dir1Compliant += count;
                    } else {
                        dir1NonCompliant += count;
                    }
                } catch (error) {
                    console.warn("Error processing speed column:", col, error);
                }
            }
        }

        // Process direction 2 speed compliance
        if (structure.dir2SpeedCols && Array.isArray(structure.dir2SpeedCols)) {
            for (const col of structure.dir2SpeedCols) {
                try {
                    const speedValue = extractSpeedFromColumn(col);
                    const count = processedRow[col] || 0;

                    if (speedValue <= speedLimit) {
                        dir2Compliant += count;
                    } else {
                        dir2NonCompliant += count;
                    }
                } catch (error) {
                    console.warn("Error processing speed column:", col, error);
                }
            }
        }

        processedRow.Dir1_Compliant = dir1Compliant;
        processedRow.Dir1_Non_Compliant = dir1NonCompliant;
        processedRow.Dir2_Compliant = dir2Compliant;
        processedRow.Dir2_Non_Compliant = dir2NonCompliant;

        return processedRow;
    });
}

/**
 * Extract speed value from column name (e.g., "35-39 MPH" -> 35)
 */
function extractSpeedFromColumn(columnName) {
    try {
        const speedPart = columnName.split("MPH")[0].trim();
        if (speedPart.includes("+")) {
            return parseFloat(speedPart.replace("+", "").trim());
        } else {
            return parseFloat(speedPart.split("-")[0].trim());
        }
    } catch (error) {
        console.warn(`Could not extract speed from column: ${columnName}`);
        return 0;
    }
}