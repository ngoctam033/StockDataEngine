-- tạo một table để lưu dữ liệu chứng khoáng
-- có các trường sau: ticker, vol, now, date
-- ticker: mã chứng khoán
-- vol: khối lượng giao dịch
-- now: giá hiện tại
-- date: ngày , giờ giao dịch
CREATE TABLE IF NOT EXISTS stock_data (
    -- ticker có kiểu dữ liệu là varchar(10) và không được null
    ticker varchar(10) NOT NULL,
    -- vol có kiểu dữ liệu là int và không được null
    vol int NOT NULL,
    -- now có kiểu dữ liệu là float và không được null
    now float NOT NULL,
    -- date có kiểu dữ liệu là timestamp và không được null
    date timestamp NOT NULL,
    -- tạo một id tự tăng
    id SERIAL PRIMARY KEY
);

-- tạo một bảng để lưu dữ liệu chứng khoán đã được phân tích
-- có các trường sau: ticker, date, open, hight, low, close, vol
-- ticker: mã chứng khoán, kiểu dữ liệu là varchar(10) và không được null
-- date: ngày giao dịch, kiểu dữ liệu là datetime và không được null
-- open: giá mở cửa, kiểu dữ liệu là int và không được null
-- hight: giá cao nhất, kiểu dữ liệu là int và không được null
-- low: giá thấp nhất, kiểu dữ liệu là int và không được null
-- close: giá đóng cửa, kiểu dữ liệu là int và không được null
-- vol: khối lượng giao dịch trong ngày, kiểu dữ liệu là int và không được null
CREATE TABLE IF NOT EXISTS stock_data_analyzed (
    ticker varchar(10) NOT NULL,
    date timestamp NOT NULL,
    open float NOT NULL,
    hight float NOT NULL,
    low float NOT NULL,
    close float NOT NULL,
    vol int NOT NULL,
    id SERIAL PRIMARY KEY
);