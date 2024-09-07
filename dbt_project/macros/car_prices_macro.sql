{% macro generate_car_prices() %}

WITH manufacturers_and_cars AS (
    SELECT
        m.manufacturer_id as m_id,
        m.manufacturer_name as m_name,
        c.model as c_model,
        c.price as c_price
    FROM {{ ref('manufacturers') }} m
    LEFT JOIN {{ ref('manufacturers_cars') }} cm ON m.manufacturer_id = cm.manufacturer_id
    LEFT JOIN {{ ref('cars') }} c ON cm.car_id = c.car_id
    GROUP BY m.manufacturer_id, m.manufacturer_name, c.model, c.price
)

SELECT
    m_id,
    m_name,
    AVG(c_price)
FROM
    manufacturers_and_cars
GROUP BY m_id, m_name

{% endmacro %}