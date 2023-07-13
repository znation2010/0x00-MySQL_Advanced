-- Lists all bands with Glam as their main style, ranked by their longevity
SELECT band_name,
    YEAR('2020-01-01') - CAST(SUBSTRING_INDEX(split, ' - ', 1) AS SIGNED) AS lifespan
FROM metal_bands
WHERE band_name IN (
    SELECT band_name
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', style) > 0
)
ORDER BY lifespan DESC;
