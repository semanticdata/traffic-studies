/**
 * HourlyData component for providing hardcoded hourly traffic data
 * Following Observable Framework best practices for data handling
 * @returns {Array} - Array of hourly traffic data objects
 */
export function getHourlyData() {
  return [
    {hour: 0, northbound: 8, southbound: 7, total: 15},
    {hour: 1, northbound: 5, southbound: 3, total: 8},
    {hour: 2, northbound: 4, southbound: 2, total: 6},
    {hour: 3, northbound: 2, southbound: 1, total: 3},
    {hour: 4, northbound: 3, southbound: 2, total: 5},
    {hour: 5, northbound: 12, southbound: 8, total: 20},
    {hour: 6, northbound: 45, southbound: 32, total: 77},
    {hour: 7, northbound: 125, southbound: 89, total: 214},
    {hour: 8, northbound: 189, southbound: 145, total: 334},
    {hour: 9, northbound: 156, southbound: 123, total: 279},
    {hour: 10, northbound: 134, southbound: 112, total: 246},
    {hour: 11, northbound: 145, southbound: 132, total: 277},
    {hour: 12, northbound: 167, southbound: 156, total: 323},
    {hour: 13, northbound: 189, southbound: 178, total: 367},
    {hour: 14, northbound: 234, southbound: 189, total: 423},
    {hour: 15, northbound: 298, southbound: 234, total: 532},
    {hour: 16, northbound: 456, southbound: 409, total: 865},
    {hour: 17, northbound: 389, southbound: 334, total: 723},
    {hour: 18, northbound: 278, southbound: 245, total: 523},
    {hour: 19, northbound: 198, southbound: 178, total: 376},
    {hour: 20, northbound: 156, southbound: 134, total: 290},
    {hour: 21, northbound: 123, southbound: 98, total: 221},
    {hour: 22, northbound: 89, southbound: 67, total: 156},
    {hour: 23, northbound: 45, southbound: 32, total: 77}
  ];
}