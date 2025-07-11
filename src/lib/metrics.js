/**
 * Metrics calculation utilities for Traffic Studies dashboard.
 * 
 * This module contains functions to calculate various traffic metrics and KPIs
 * from the processed traffic data, converted from Python to JavaScript.
 */

/**
 * Calculate the weighted average speed
 * @param {Array} data - Traffic data array
 * @param {Array} speedCols - Array of speed column names
 * @returns {number} Weighted average speed
 */
export function calculateWeightedSpeed(data, speedCols) {
    let totalCount = 0;
    let weightedSum = 0;
    
    for (const col of speedCols) {
        try {
            // Extract speed from column name, handle formats like "25-29 MPH" and "45+ MPH"
            const speedPart = col.split("MPH")[0].trim();
            let speed;
            
            if (speedPart.includes("+")) {
                // Handle "45+" format - use the number as-is
                speed = parseFloat(speedPart.replace("+", "").trim());
            } else {
                // Handle "25-29" format - use lower bound
                speed = parseFloat(speedPart.split("-")[0].trim());
            }
            
            const count = data.reduce((sum, row) => sum + (row[col] || 0), 0);
            weightedSum += speed * count;
            totalCount += count;
        } catch (error) {
            // Skip columns that don't have valid speed format
            console.warn(`Could not parse speed from column: ${col}`);
            continue;
        }
    }
    
    return totalCount > 0 ? weightedSum / totalCount : 0;
}

/**
 * Calculate the number of compliant and non-compliant vehicles
 * @param {Array} data - Traffic data array
 * @param {Array} speedCols - Array of speed column names
 * @param {number} speedLimit - Speed limit in MPH
 * @returns {Object} Object with compliant and total counts
 */
export function calculateCompliance(data, speedCols, speedLimit = 30) {
    let compliant = 0;
    let total = 0;
    
    for (const col of speedCols) {
        try {
            // Extract speed from column name
            const speedPart = col.split("MPH")[0].trim();
            let speed;
            
            if (speedPart.includes("+")) {
                speed = parseFloat(speedPart.replace("+", "").trim());
            } else {
                speed = parseFloat(speedPart.split("-")[0].trim());
            }
            
            const count = data.reduce((sum, row) => sum + (row[col] || 0), 0);
            
            if (speed <= speedLimit) {
                compliant += count;
            }
            total += count;
        } catch (error) {
            console.warn(`Could not parse speed from column: ${col}`);
            continue;
        }
    }
    
    return { compliant, total };
}

/**
 * Calculate the 85th percentile speed (optimized to avoid memory issues)
 * @param {Array} data - Traffic data array
 * @param {Array} speedCols - Array of speed column names
 * @returns {number} 85th percentile speed
 */
export function calculate85thPercentileSpeed(data, speedCols) {
    const speedBins = new Map(); // Use Map for efficient speed bin counting
    let totalVehicles = 0;
    
    // Count vehicles in each speed bin
    for (const col of speedCols) {
        try {
            const speedPart = col.split("MPH")[0].trim();
            let lower, upper;
            
            if (speedPart.includes("+")) {
                // Handle "45+" format - use the number plus 5 as upper bound
                lower = parseFloat(speedPart.replace("+", "").trim());
                upper = lower + 5; // Assume +5 mph range for "+" speeds
            } else {
                // Handle "25-29" format
                const speedRange = speedPart.split("-");
                lower = parseFloat(speedRange[0].trim());
                upper = speedRange.length > 1 ? parseFloat(speedRange[1].trim()) : lower;
            }
            
            const midSpeed = (lower + upper) / 2;
            const count = data.reduce((sum, row) => sum + (row[col] || 0), 0);
            
            // Use midSpeed as key and accumulate counts
            speedBins.set(midSpeed, (speedBins.get(midSpeed) || 0) + count);
            totalVehicles += count;
        } catch (error) {
            console.warn(`Could not parse speed from column: ${col}`);
            continue;
        }
    }
    
    if (totalVehicles === 0) return 0;
    
    // Calculate 85th percentile using cumulative distribution
    const sortedSpeeds = Array.from(speedBins.keys()).sort((a, b) => a - b);
    const target85th = totalVehicles * 0.85;
    let cumulativeCount = 0;
    
    for (const speed of sortedSpeeds) {
        cumulativeCount += speedBins.get(speed);
        if (cumulativeCount >= target85th) {
            return speed;
        }
    }
    
    // Fallback to highest speed if we somehow don't reach 85th percentile
    return sortedSpeeds[sortedSpeeds.length - 1] || 0;
}

/**
 * Calculate the Peak Hour Factor (PHF)
 * @param {Array} data - Traffic data array
 * @returns {number} Peak Hour Factor
 */
export function calculatePHF(data) {
    const hourlyVolumes = {};
    
    // Calculate hourly volumes
    data.forEach(row => {
        const hour = row.Hour;
        if (hour !== null && hour !== undefined) {
            hourlyVolumes[hour] = (hourlyVolumes[hour] || 0) + (row.Total || 0);
        }
    });
    
    const volumes = Object.values(hourlyVolumes);
    if (volumes.length === 0) return 0;
    
    const peakHourVolume = Math.max(...volumes);
    if (peakHourVolume === 0) return 0;
    
    // For simplification, assuming 15-minute intervals would be 1/4 of hourly
    // In real implementation, would need 15-minute data
    const peak15min = peakHourVolume * 4; // This is a simplified calculation
    
    return peakHourVolume / peak15min;
}

/**
 * Count the number of high-speed violators (15+ mph over limit)
 * @param {Array} data - Traffic data array
 * @param {Array} speedCols - Array of speed column names
 * @param {number} speedLimit - Speed limit in MPH
 * @returns {number} Number of high-speed violators
 */
export function countHighSpeeders(data, speedCols, speedLimit = 30) {
    let highSpeeders = 0;
    
    for (const col of speedCols) {
        try {
            // Extract speed from column name
            const speedPart = col.split("MPH")[0].trim();
            let speed;
            
            if (speedPart.includes("+")) {
                speed = parseFloat(speedPart.replace("+", "").trim());
            } else {
                speed = parseFloat(speedPart.split("-")[0].trim());
            }
            
            if (speed >= speedLimit + 15) {
                highSpeeders += data.reduce((sum, row) => sum + (row[col] || 0), 0);
            }
        } catch (error) {
            console.warn(`Could not parse speed from column: ${col}`);
            continue;
        }
    }
    
    return highSpeeders;
}

/**
 * Calculate all core metrics for the dashboard (optimized version)
 * @param {Array} data - Filtered traffic data array
 * @param {Object} structure - Data structure information
 * @param {number} speedLimit - Speed limit in MPH
 * @returns {Object} Object containing all calculated metrics
 */
export function getCoreMetrics(data, structure, speedLimit = 30) {
    // Early return if no data
    if (!data || data.length === 0) {
        return {
            totalVehicles: 0,
            combinedAvgSpeed: 0,
            complianceRate: 0,
            percentile85th: 0,
            peakHour: 0,
            peakVehicles: 0,
            dominantDirection: structure.dir1Name || "Unknown",
            dominantPct: 0
        };
    }
    
    // Single pass through data to collect all needed values
    let totalVehicles = 0;
    let dir1Volume = 0;
    let dir2Volume = 0;
    const hourlyVolumes = {};
    
    // Collect basic stats in one pass
    data.forEach(row => {
        const total = row.Total || 0;
        const vol1 = row[structure.dir1VolumeCol] || 0;
        const vol2 = row[structure.dir2VolumeCol] || 0;
        
        totalVehicles += total;
        dir1Volume += vol1;
        dir2Volume += vol2;
        
        // Track hourly volumes
        const hour = row.Hour;
        if (hour !== null && hour !== undefined) {
            hourlyVolumes[hour] = (hourlyVolumes[hour] || 0) + total;
        }
    });
    
    // Speed calculations (these are already optimized)
    const dir1AvgSpeed = calculateWeightedSpeed(data, structure.dir1SpeedCols || []);
    const dir2AvgSpeed = calculateWeightedSpeed(data, structure.dir2SpeedCols || []);
    const combinedAvgSpeed = (dir1AvgSpeed + dir2AvgSpeed) / 2;
    
    // Compliance calculations
    const dir1Compliance = calculateCompliance(data, structure.dir1SpeedCols || [], speedLimit);
    const dir2Compliance = calculateCompliance(data, structure.dir2SpeedCols || [], speedLimit);
    const totalCompliant = dir1Compliance.compliant + dir2Compliance.compliant;
    const totalSpeedReadings = dir1Compliance.total + dir2Compliance.total;
    const complianceRate = totalSpeedReadings > 0 ? (totalCompliant / totalSpeedReadings * 100) : 0;
    
    // 85th percentile speed (optimized version)
    const dir185th = calculate85thPercentileSpeed(data, structure.dir1SpeedCols || []);
    const dir285th = calculate85thPercentileSpeed(data, structure.dir2SpeedCols || []);
    const percentile85th = Math.max(dir185th, dir285th);
    
    // Peak hour analysis
    const peakHourEntry = Object.entries(hourlyVolumes)
        .reduce((max, [hour, volume]) => volume > max.volume ? {hour: parseInt(hour), volume} : max, 
                {hour: 0, volume: 0});
    
    // Dominant direction
    const dominantDirection = dir1Volume > dir2Volume ? structure.dir1Name : structure.dir2Name;
    const dominantPct = (dir1Volume + dir2Volume) > 0 ? 
        (Math.max(dir1Volume, dir2Volume) / (dir1Volume + dir2Volume) * 100) : 0;
    
    return {
        totalVehicles,
        combinedAvgSpeed,
        complianceRate,
        percentile85th,
        peakHour: peakHourEntry.hour,
        peakVehicles: peakHourEntry.volume,
        dominantDirection,
        dominantPct
    };
}