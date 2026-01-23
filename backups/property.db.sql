BEGIN TRANSACTION;
DROP TABLE IF EXISTS "account";
CREATE TABLE "account" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "class_assets";
CREATE TABLE "class_assets" (
	"id"	INTEGER NOT NULL UNIQUE,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"desc"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "fof_strategy";
CREATE TABLE "fof_strategy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"acccount_id"	INTEGER,
	"currency_id"	INTEGER,
	"four_type_money_id"	INTEGER,
	"class_assets_id"	INTEGER,
	"type_assets_id"	INTEGER DEFAULT 3,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("acccount_id") REFERENCES "account"("id"),
	FOREIGN KEY("class_assets_id") REFERENCES "class_assets"("id"),
	FOREIGN KEY("currency_id") REFERENCES "foreign_exchange"("id"),
	FOREIGN KEY("four_type_money_id") REFERENCES "four_type_money"("id"),
	FOREIGN KEY("type_assets_id") REFERENCES "type_assets"("id")
);
DROP TABLE IF EXISTS "foreign_exchange";
CREATE TABLE "foreign_exchange" (
	"id"	INTEGER NOT NULL UNIQUE,
	"currency"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "foreign_exchange_rate";
CREATE TABLE "foreign_exchange_rate" (
	"id"	INTEGER NOT NULL UNIQUE,
	"currency_id"	INTEGER NOT NULL,
	"rate"	NUMERIC NOT NULL,
	"date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("currency_id") REFERENCES "foreign_exchange"("id")
);
DROP TABLE IF EXISTS "four_type_money";
CREATE TABLE "four_type_money" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "fund";
CREATE TABLE "fund" (
	"id"	INTEGER NOT NULL UNIQUE,
	"market_id"	INTEGER,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"currency_id"	INTEGER,
	"four_type_money_id"	INTEGER,
	"class_assets_id"	INTEGER,
	"type_assets_id"	INTEGER DEFAULT 2,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("class_assets_id") REFERENCES "class_assets"("id"),
	FOREIGN KEY("currency_id") REFERENCES "foreign_exchange"("id"),
	FOREIGN KEY("four_type_money_id") REFERENCES "four_type_money"("id"),
	FOREIGN KEY("market_id") REFERENCES "market"("id"),
	FOREIGN KEY("type_assets_id") REFERENCES "type_assets"("id")
);
DROP TABLE IF EXISTS "fund_net_asset_value";
CREATE TABLE "fund_net_asset_value" (
	"id"	INTEGER NOT NULL UNIQUE,
	"fund_id"	INTEGER,
	"date"	TEXT,
	"nav"	NUMERIC,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("fund_id") REFERENCES "fund"("id")
);
DROP TABLE IF EXISTS "fund_position_holding";
CREATE TABLE "fund_position_holding" (
	"id"	INTEGER NOT NULL UNIQUE,
	"fund_id"	INTEGER,
	"position_quantity"	NUMERIC, --持仓数量。 交易记录中，买入数量-卖出数量+分红数量
	"cost_price"	NUMERIC, --持仓成本。交易记录中，（买入发生额+卖出发生额+分红发生额）取正数
	"floating_profit_loss"	NUMERIC, --浮动盈亏
	"profit_loss_percentage"	NUMERIC, --浮动盈亏百分比
	"annualized_return"	NUMERIC, --年化收益率
	"date"	TEXT,  --日期 yyyy-mm-dd
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("fund_id") REFERENCES "fund"("id")
);
DROP TABLE IF EXISTS "fund_transactions";
CREATE TABLE "fund_transactions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_date"	TEXT,
	"fund_id"	INTEGER,
	"type_transction_id"	INTEGER,
	"quantity"	NUMERIC,
	"price"	NUMERIC,
	"turnover"	NUMERIC,
	"fee"	NUMERIC,
	"transaction_amount"	NUMERIC,
	"account_id"	INTEGER,
	"notes"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("account_id") REFERENCES "account"("id"),
	FOREIGN KEY("fund_id") REFERENCES "fund"("id"),
	FOREIGN KEY("type_transction_id") REFERENCES "type_transaction"("id")
);
DROP TABLE IF EXISTS "market";
CREATE TABLE "market" (
	"id"	INTEGER NOT NULL UNIQUE,
	"code"	TEXT,
	"name"	TEXT,
	"desc"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "stock";
CREATE TABLE "stock" (
	"id"	INTEGER NOT NULL UNIQUE,
	"market_id"	INTEGER,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"currency_id"	INTEGER,
	"four_type_money_id"	INTEGER,
	"class_assets_id"	INTEGER,
	"type_assets_id"	INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("class_assets_id") REFERENCES "class_assets"("id"),
	FOREIGN KEY("currency_id") REFERENCES "foreign_exchange"("id"),
	FOREIGN KEY("four_type_money_id") REFERENCES "four_type_money"("id"),
	FOREIGN KEY("market_id") REFERENCES "market"("id"),
	FOREIGN KEY("type_assets_id") REFERENCES "type_assets"("id")
);
DROP TABLE IF EXISTS "stock_net_asset_value";
CREATE TABLE "stock_net_asset_value" (
	"id"	INTEGER NOT NULL UNIQUE,
	"stock_id"	INTEGER,
	"date"	TEXT,
	"nav"	NUMERIC,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("stock_id") REFERENCES "stock"("id")
);
DROP TABLE IF EXISTS "stock_position_holding";
CREATE TABLE "stock_position_holding" (
	"id"	INTEGER NOT NULL UNIQUE,
	"stock_id"	INTEGER,
	"position_quantity"	NUMERIC,
	"cost_price"	NUMERIC,
	"floating_profit_loss"	NUMERIC,
	"profit_loss_percentage"	NUMERIC,
	"annualized_return"	NUMERIC,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("stock_id") REFERENCES "stock"("id")
);
DROP TABLE IF EXISTS "stock_transactions";
CREATE TABLE "stock_transactions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_date"	TEXT,
	"stock_id"	INTEGER,
	"type_transction_id"	INTEGER,
	"quantity"	NUMERIC,
	"price"	NUMERIC,
	"turnover"	NUMERIC,
	"fee"	NUMERIC,
	"transaction_amount"	NUMERIC,
	"account_id"	INTEGER,
	"notes"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("account_id") REFERENCES "account"("id"),
	FOREIGN KEY("stock_id") REFERENCES "stock"("id"),
	FOREIGN KEY("type_transction_id") REFERENCES "type_transaction"("id"),
	FOREIGN KEY("type_transction_id") REFERENCES "type_transaction"("id")
);
DROP TABLE IF EXISTS "type_assets";
CREATE TABLE "type_assets" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "type_transaction";
CREATE TABLE "type_transaction" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "account" ("id","name") VALUES (1,'且慢');
INSERT INTO "account" ("id","name") VALUES (2,'天天基金');
INSERT INTO "account" ("id","name") VALUES (3,'雪球');
INSERT INTO "account" ("id","name") VALUES (4,'银河');
INSERT INTO "account" ("id","name") VALUES (5,'招行');
INSERT INTO "account" ("id","name") VALUES (6,'中行');
INSERT INTO "account" ("id","name") VALUES (7,'万通保险YFLife');
INSERT INTO "account" ("id","name") VALUES (8,'中银香港');
INSERT INTO "account" ("id","name") VALUES (9,'华盛通');
INSERT INTO "account" ("id","name") VALUES (10,'IBKR');
INSERT INTO "account" ("id","name") VALUES (11,'Schwab');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (1,'010000','权益类','包括股票、股票型基金、混合型基金偏股部分等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (2,'020000','固定收益类','债券、债券基金、货币基金等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (3,'030000','现金及等价物',NULL);
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (4,'040000','另类投资','如黄金、房地产等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (5,'010100','主动管理','权益类内部，包括您自己选的股票、主动管理型基金');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (6,'010200','被动指数','权益类内部，包括宽基指数、行业指数、主题指数、策略指数等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (7,'010300','基金顾投',NULL);
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (8,'010201','宽基指数','沪深300、中证500等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (9,'010202','行业/主题指数','消费、医药、科技等');
INSERT INTO "class_assets" ("id","code","name","desc") VALUES (10,'010203','策略指数','红利、低波动、自由现金流等');
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (1,'长赢指数投资计划-S定投',1,1,1,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (2,'长赢指数投资计划-150份',1,1,1,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (3,'且慢定制方案',1,1,1,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (4,'我要稳稳的幸福',1,1,2,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (5,'天马稳健',1,1,2,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (6,'雪球长线账户',3,1,1,7,3);
INSERT INTO "fof_strategy" ("id","name","acccount_id","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (7,'雪球稳钱账户',3,1,2,7,3);
INSERT INTO "foreign_exchange" ("id","currency") VALUES (1,'CNY');
INSERT INTO "foreign_exchange" ("id","currency") VALUES (2,'USD');
INSERT INTO "foreign_exchange" ("id","currency") VALUES (3,'HKD');
INSERT INTO "foreign_exchange_rate" ("id","currency_id","rate","date") VALUES (1,2,6.9821,'2026-01-12');
INSERT INTO "foreign_exchange_rate" ("id","currency_id","rate","date") VALUES (4,2,6.9929,'2026-01-23');
INSERT INTO "foreign_exchange_rate" ("id","currency_id","rate","date") VALUES (5,3,0.8968,'2026-01-23');
INSERT INTO "four_type_money" ("id","name") VALUES (1,'长钱');
INSERT INTO "four_type_money" ("id","name") VALUES (2,'稳钱');
INSERT INTO "four_type_money" ("id","name") VALUES (3,'活钱');
INSERT INTO "four_type_money" ("id","name") VALUES (4,'保险');
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (1,2,'159232','自由现金流ETF南方',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (2,1,'563020','红利低波动ETF',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (3,1,'512480','半导体ETF',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (4,1,'513180','恒生科技指数ETF',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (5,1,'515080','中证红利ETF',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (6,1,'515100','红利低波100ETF',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (7,1,'518880','黄金ETF',1,1,4,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (8,1,'563900','沪深300自由现金流ETF摩根',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (9,4,'017559','华安上证科创板芯片ETF联接A',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (10,4,'160119','南方中证500ETF联接A',1,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (11,4,'004253','国泰黄金ETF联接C',1,1,4,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (12,4,'005550','汇安成长优选A',1,1,5,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (13,4,'000968','广发中证养老产业A',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (14,4,'501210','交银智选星光A',1,1,5,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (15,4,'519710','交银策略回报',1,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (16,4,'010094','交银产业机遇',1,1,5,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (17,4,'017512','广发北证50成份A',1,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (18,4,'001717','工银前沿医疗A',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (19,4,'003634','嘉实农业产业A',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (20,4,'004813','中欧先进制造C',1,1,9,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (21,4,'000609','华商新量化A',1,1,5,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (22,4,'110020','易方达沪深300ETF联接A',1,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (23,5,'DIV','Global X附加股息美国ETF',2,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (24,5,'QQQ','Invesco QQQ纳指100ETF',2,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (25,5,'SDIV','Global X超级红利ETF',2,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (26,5,'SPY','SPDR标普500指数ETF',2,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (27,5,'SPYD','SS SPDR标普500高股息ETF',2,1,10,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (28,4,'015453','中欧中证500指数增强A',1,1,8,2);
INSERT INTO "fund" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (29,4,'020156','交银中证红利低波动100指数A',1,1,10,2);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (1,1,'2026-01-13',1.288);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (2,2,'2026-01-13',1.1797);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (3,3,'2026-01-13',1.6167);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (4,4,'2026-01-13',0.7547);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (5,5,'2026-01-13',1.5726);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (6,6,'2026-01-13',1.4333);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (7,7,'2026-01-13',9.5869);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (8,8,'2026-01-13',1.1956);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (9,9,'2026-01-13',2.3723);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (10,10,'2026-01-13',2.2556);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (11,11,'2026-01-13',3.544);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (12,12,'2026-01-13',2.655);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (13,13,'2026-01-13',0.986);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (14,14,'2026-01-13',1.0856);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (15,15,'2026-01-13',1.471);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (16,16,'2026-01-13',1.0814);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (17,17,'2026-01-13',1.7998);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (18,18,'2026-01-13',3.398);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (19,19,'2026-01-13',1.3504);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (20,20,'2026-01-13',2.8124);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (21,21,'2026-01-13',2.606);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (22,22,'2026-01-13',1.9086);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (23,23,'2026-01-13',17.72);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (24,24,'2026-01-13',626.7923);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (25,25,'2026-01-13',24.7);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (26,26,'2026-01-13',694.066);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (27,27,'2026-01-13',44.3461);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (28,28,'2026-01-13',1.4918);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (29,29,'2026-01-13',1.1428);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (64,1,'2026-01-22',1.3284);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (65,2,'2026-01-22',1.1724);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (66,3,'2026-01-22',1.7319);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (67,4,'2026-01-22',0.7634);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (68,5,'2026-01-22',1.5807);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (69,6,'2026-01-22',1.4314);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (70,7,'2026-01-22',10.3509);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (71,8,'2026-01-22',1.2048);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (72,9,'2026-01-22',2.5245);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (73,10,'2026-01-22',2.3448);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (74,11,'2026-01-22',3.8254);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (75,12,'2026-01-22',2.773);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (76,13,'2026-01-22',0.9722);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (77,14,'2026-01-21',1.1305);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (78,15,'2026-01-22',1.448);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (79,16,'2026-01-22',1.0888);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (80,17,'2026-01-22',1.8063);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (81,18,'2026-01-22',3.14);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (82,19,'2026-01-22',1.3112);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (83,20,'2026-01-22',2.8305);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (84,21,'2026-01-22',2.672);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (85,22,'2026-01-22',1.8969);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (86,23,'2026-01-22',18.21);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (87,24,'2026-01-22',620.76);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (88,25,'2026-01-22',25.65);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (89,26,'2026-01-22',688.98);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (90,27,'2026-01-22',45.09);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (91,28,'2026-01-22',1.5605);
INSERT INTO "fund_net_asset_value" ("id","fund_id","date","nav") VALUES (92,29,'2026-01-22',1.1384);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (1,'2020-09-01',26,1,1,350.85,350.85,1.8,-352.65,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (2,'2020-09-01',24,1,1,298.06,298.06,1.8,-299.86,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (3,'2020-10-01',25,1,10,10.77,107.7,1.82,-109.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (4,'2020-10-01',23,1,10,15.13,151.3,1.82,-153.12,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (5,'2020-10-01',27,1,10,27.37,273.7,1.82,-275.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (6,'2020-10-14',25,3,0,0,0.8,0.24,0.56,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (7,'2020-10-14',23,3,0,0,1,0.3,0.7,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (8,'2020-11-02',26,3,0,0,1.33,0.4,0.93,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (9,'2020-11-02',24,3,0,0,0.38,0.11,0.27,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (10,'2020-11-13',25,3,0,0,0.76,0.22,0.54,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (11,'2020-11-13',23,3,0,0,1,0.3,0.7,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (12,'2020-12-14',25,3,0,0,0.76,0.22,0.54,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (13,'2020-12-14',23,3,0,0,0.99,0.3,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (14,'2020-12-24',27,3,0,0,6.06,1.82,4.24,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (15,'2020-12-31',23,1,3,16.67,50.01,1.8,-51.81,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (16,'2021-01-04',24,3,0,0,0.56,0.16,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (17,'2021-01-08',21,1,3413.68,2.925,9985.014,14.98,-10000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (18,'2021-01-11',25,3,0,0,0.75,0.22,0.53,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (19,'2021-01-11',23,3,0,0,1,0.3,0.7,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (20,'2021-02-01',26,3,0,0,1.58,0.47,1.11,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (21,'2021-02-12',25,3,0,0,0.75,0.08,0.67,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (22,'2021-02-12',23,3,0,0,1.29,0.13,1.16,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (23,'2021-03-04',21,1,3780.77,2.641,9985.01357,14.98,-10000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (24,'2021-03-12',25,3,0,0,0.8,0.08,0.72,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (25,'2021-03-12',23,3,0,0,1.2,0.12,1.08,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (26,'2021-03-25',27,3,0,0,6.36,0.64,5.72,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (27,'2021-04-14',25,3,0,0,0.88,0.09,0.79,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (28,'2021-04-14',23,3,0,0,1.15,0.11,1.04,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (29,'2021-05-03',26,3,0,0,1.27,0.12,1.15,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (30,'2021-05-03',24,3,0,0,0.39,0.03,0.36,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (31,'2021-05-06',22,1,547.71,1.8236,998.803956,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (32,'2021-05-14',25,3,0,0,0.88,0.09,0.79,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (33,'2021-05-14',23,3,0,0,1.15,0.12,1.03,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (34,'2021-05-31',22,1,527.82,1.8923,998.793786,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (35,'2021-06-12',25,3,0,0,0.88,0.09,0.79,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (36,'2021-06-12',23,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (37,'2021-06-24',27,3,0,0,3.98,0.4,3.58,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (38,'2021-06-30',22,1,536.73,1.8609,998.800857,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (39,'2021-07-15',25,3,0,0,0.88,0.09,0.79,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (40,'2021-07-15',23,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (41,'2021-07-29',22,1,578.28,1.7272,998.805216,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (42,'2021-08-02',26,3,0,0,1.37,0.13,1.24,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (43,'2021-08-02',24,3,0,0,0.39,0.03,0.36,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (44,'2021-08-13',25,3,0,0,0.9,0.09,0.81,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (45,'2021-08-13',23,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (46,'2021-09-14',10,1,6957.86,2.0097,13983.211242,16.78,-14000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (47,'2021-09-15',25,3,0,0,0.9,0.09,0.81,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (48,'2021-09-15',23,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (49,'2021-09-23',27,3,0,0,3.86,0.38,3.48,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (50,'2021-09-29',22,1,561.5,1.7788,998.7962,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (51,'2021-10-14',25,3,0,0,0.9,0.09,0.81,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (52,'2021-10-14',23,3,0,0,1.19,0.12,1.07,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (53,'2021-10-14',10,1,542.53,1.841,998.79773,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (54,'2021-10-19',10,1,536.24,1.8626,998.800624,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (55,'2021-11-01',26,3,0,0,1.42,0.14,1.28,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (56,'2021-11-01',24,3,0,0,0.41,0.04,0.37,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (57,'2021-11-15',25,3,0,0,0.9,0.09,0.81,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (58,'2021-11-15',23,3,0,0,1.18,0.12,1.06,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (59,'2021-11-16',10,1,533.83,1.871,998.79593,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (60,'2021-11-18',10,1,533.38,1.8726,998.807388,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (61,'2021-12-01',22,1,566.28,1.7638,998.804664,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (62,'2021-12-09',10,1,519.1,1.9241,998.80031,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (63,'2021-12-14',25,3,0,0,1,0.1,0.9,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (64,'2021-12-14',23,3,0,0,1.3,0.13,1.17,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (65,'2021-12-23',27,3,0,0,1.27,0.12,1.15,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (66,'2022-01-03',24,3,0,0,0.49,0.04,0.45,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (67,'2022-01-10',25,3,0,0,1.31,0.13,1.18,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (68,'2022-01-10',23,3,0,0,1.3,0.13,1.17,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (69,'2022-01-27',18,1,274.31,3.64,998.4884,1.5,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (70,'2022-01-27',10,1,557.18,1.7926,998.800868,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (71,'2022-02-01',26,3,0,0,1.63,0.16,1.47,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (72,'2022-02-07',22,1,597.08,1.6728,998.795424,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (73,'2022-02-14',25,3,0,0,1,0.1,0.9,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (74,'2022-02-14',23,3,0,0,1.2,0.12,1.08,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (75,'2022-03-01',22,1,594.77,1.6793,998.797261,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (76,'2022-03-14',25,3,0,0,1,0.1,0.9,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (77,'2022-03-14',23,3,0,0,1.2,0.12,1.08,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (78,'2022-03-14',10,1,582.29,1.7153,998.802037,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (79,'2022-03-16',25,1,1,10.46,10.46,1.8,-12.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (80,'2022-03-18',10,1,600.6,1.663,998.7978,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (81,'2022-03-24',27,3,0,0,6.52,0.65,5.87,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (82,'2022-04-11',22,1,641.41,1.5572,998.803652,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (83,'2022-04-14',25,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (84,'2022-04-14',23,3,0,0,1.3,0.13,1.17,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (85,'2022-04-22',10,1,649.8,1.5371,998.80758,1.2,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (86,'2022-04-22',22,1,677.15,1.475,998.79625,1.2,-1000,2,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (87,'2022-05-02',26,3,0,0,1.36,0.13,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (88,'2022-05-02',24,3,0,0,0.43,0.04,0.39,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (89,'2022-05-13',25,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (90,'2022-05-13',23,3,0,0,1.35,0.14,1.21,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (91,'2022-06-14',25,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (92,'2022-06-14',23,3,0,0,1.35,0.14,1.21,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (93,'2022-06-24',27,3,0,0,4.04,0.4,3.64,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (94,'2022-07-15',25,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (95,'2022-07-15',23,3,0,0,1.35,0.14,1.21,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (96,'2022-07-26',19,1,584.19,2.103,1228.55157,0,-1228.55157,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (97,'2022-07-26',20,1,168.11,3.3085,556.191935,0,-556.191935,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (98,'2022-08-01',26,3,0,0,1.57,0.15,1.42,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (99,'2022-08-01',24,3,0,0,0.52,0.05,0.47,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (100,'2022-08-12',25,3,0,0,1.1,0.11,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (101,'2022-08-12',23,3,0,0,1.37,0.14,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (102,'2022-09-15',25,3,0,0,1.04,0.1,0.94,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (103,'2022-09-15',23,3,0,0,1.4,0.14,1.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (104,'2022-09-22',27,3,0,0,4.18,0.41,3.77,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (105,'2022-10-14',25,3,0,0,0.93,0.09,0.84,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (106,'2022-10-14',23,3,0,0,1.4,0.14,1.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (107,'2022-11-01',26,3,0,0,1.59,0.16,1.43,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (108,'2022-11-01',24,3,0,0,0.51,0.05,0.46,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (109,'2022-11-11',25,3,0,0,0.93,0.09,0.84,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (110,'2022-11-11',23,3,0,0,1.4,0.14,1.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (111,'2022-12-14',25,3,0,0,0.93,0.09,0.84,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (112,'2022-12-14',23,3,0,0,1.4,0.14,1.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (113,'2022-12-22',27,3,0,0,5.07,0.5,4.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (114,'2023-01-03',24,3,0,0,0.65,0.06,0.59,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (115,'2023-01-06',23,3,0,0,16.24,0,16.24,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (116,'2023-01-10',25,3,0,0,0.76,0.07,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (117,'2023-01-10',23,3,0,0,1.4,0.14,1.26,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (118,'2023-02-01',26,3,0,0,1.78,0.17,1.61,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (119,'2023-02-14',25,3,0,0,0.76,0.07,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (120,'2023-02-14',23,3,0,0,1.27,0.13,1.14,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (121,'2023-03-14',25,3,0,0,0.76,0.07,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (122,'2023-03-14',23,3,0,0,1.28,0.13,1.15,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (123,'2023-03-23',27,3,0,0,3.87,0.38,3.49,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (124,'2023-04-17',25,3,0,0,1.27,0.13,1.14,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (125,'2023-04-17',23,3,0,0,0.69,0.06,0.63,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (126,'2023-05-01',26,3,0,0,1.5,0.15,1.35,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (127,'2023-05-01',24,3,0,0,0.47,0.04,0.43,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (128,'2023-05-12',25,3,0,0,0.64,0.06,0.58,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (129,'2023-05-12',23,3,0,0,1.27,0.13,1.14,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (130,'2023-06-14',25,3,0,0,0.64,0.06,0.58,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (131,'2023-06-14',23,3,0,0,1.27,0.13,1.14,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (132,'2023-06-23',27,3,0,0,4.65,0.46,4.19,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (133,'2023-07-17',25,3,0,0,0.64,0.06,0.58,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (134,'2023-07-17',23,3,0,0,1.36,0.14,1.22,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (135,'2023-08-14',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (136,'2023-08-14',23,3,0,0,1.36,0.14,1.22,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (137,'2023-09-15',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (138,'2023-09-15',23,3,0,0,1.36,0.14,1.22,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (139,'2023-09-21',27,3,0,0,4.4,0.44,3.96,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (140,'2023-09-22',15,1,686.87,1.794,1232.24478,3.09,-1235.33478,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (141,'2023-09-22',15,1,657.17,1.794,1178.96298,2.36,-1181.32298,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (142,'2023-10-16',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (143,'2023-10-16',23,3,0,0,1.37,0.14,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (144,'2023-11-01',26,3,0,0,1.58,0.15,1.43,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (145,'2023-11-01',24,3,0,0,0.53,0.05,0.48,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (146,'2023-11-14',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (147,'2023-11-14',23,3,0,0,1.37,0.14,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (148,'2023-12-14',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (149,'2023-12-14',23,3,0,0,1.37,0.14,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (150,'2023-12-21',27,3,0,0,5.33,0.53,4.8,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (151,'2024-01-03',24,3,0,0,0.8,0.08,0.72,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (152,'2024-01-09',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (153,'2024-01-09',23,3,0,0,1.37,0.14,1.23,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (154,'2024-02-01',26,3,0,0,1.9,0.19,1.71,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (155,'2024-02-14',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (156,'2024-02-14',23,3,0,0,1.21,0.13,1.08,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (157,'2024-03-14',25,3,0,0,0.63,0.06,0.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (158,'2024-03-14',23,3,0,0,1.21,0.13,1.08,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (159,'2024-03-21',27,3,0,0,3.72,0.37,3.35,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (160,'2024-04-12',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (161,'2024-04-12',23,3,0,0,1.14,0.11,1.03,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (162,'2024-05-01',26,3,0,0,1.59,0.15,1.44,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (163,'2024-05-01',24,3,0,0,0.57,0.05,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (164,'2024-05-14',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (165,'2024-05-14',23,3,0,0,1.15,0.11,1.04,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (166,'2024-06-13',25,3,0,0,0.57,0.05,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (167,'2024-06-13',23,3,0,0,1.08,0.11,0.97,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (168,'2024-06-26',27,3,0,0,4.86,0.48,4.38,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (169,'2024-07-12',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (170,'2024-07-12',23,3,0,0,1.08,0.111,0.969,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (171,'2024-08-01',26,3,0,0,1.75,0.15,1.6,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (172,'2024-08-01',24,3,0,0,0.76,0.07,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (173,'2024-08-13',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (174,'2024-08-13',23,3,0,0,1.09,0.11,0.98,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (175,'2024-09-13',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (176,'2024-09-13',23,3,0,0,1.09,0.11,0.98,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (177,'2024-09-25',27,3,0,0,4.57,0.46,4.11,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (178,'2024-10-11',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (179,'2024-10-11',23,3,0,0,1.08,0.11,0.97,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (180,'2024-11-01',26,3,0,0,1.74,0.17,1.57,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (181,'2024-11-01',24,3,0,0,0.67,0.06,0.61,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (182,'2024-11-14',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (183,'2024-11-14',23,3,0,0,1.12,0.11,1.01,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (184,'2024-12-12',25,3,0,0,0.58,0.06,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (185,'2024-12-12',23,3,0,0,1.12,0.11,1.01,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (186,'2024-12-26',27,3,0,0,5.46,0.55,4.91,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (187,'2025-01-02',24,3,0,0,0.77,0.08,0.69,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (188,'2025-01-08',25,3,0,0,0.58,0.06,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (189,'2025-01-08',23,3,0,0,1.14,0.11,1.03,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (190,'2025-01-09',24,3,0,0,0.83,0.08,0.75,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (191,'2025-02-03',26,3,0,0,1.96,0.19,1.77,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (192,'2025-02-13',25,3,0,0,0.57,0.06,0.51,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (193,'2025-02-14',23,3,0,0,1.12,0.11,1.01,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (194,'2025-03-13',25,3,0,0,0.6,0.06,0.54,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (195,'2025-03-13',23,3,0,0,1.37,0.13,1.24,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (196,'2025-03-15',23,1,5,17.45,87.25,0.35443225,-87.6,10,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (197,'2025-03-31',27,3,0,0,4.18,1.23,2.95,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (198,'2025-04-11',25,3,0,0,0.58,0.17,0.41,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (199,'2025-04-11',23,3,0,0,1.39,0.42,0.97,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (200,'2025-05-01',26,3,0,0,1.69,0.48,1.21,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (201,'2025-05-01',24,3,0,0,0.71,0.19,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (202,'2025-05-13',25,3,0,0,0.58,0.17,0.41,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (203,'2025-05-13',23,3,0,0,1.43,0.42,1.01,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (204,'2025-05-14',23,1,5,17.58,87.9,NULL,-87.9,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (205,'2025-06-11',23,3,0,0,0.55,0.06,0.49,10,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (206,'2025-06-11',23,3,0,0,0.55,0.06,0.49,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (207,'2025-06-12',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (208,'2025-06-12',23,3,0,0,1.43,0.42,1.01,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (209,'2025-06-26',27,3,0,0,5,1.5,3.5,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (210,'2025-07-11',23,3,0,0,0.55,0.06,0.49,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (211,'2025-07-14',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (212,'2025-07-14',23,3,0,0,1.43,0.43,1,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (213,'2025-07-14',23,1,0.0273,17.9,0.48867,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (214,'2025-08-01',26,3,0,0,1.76,0.52,1.24,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (215,'2025-08-01',24,3,0,0,0.59,0.17,0.42,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (216,'2025-08-12',23,3,0,0,0.54,0.05,0.49,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (217,'2025-08-13',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (218,'2025-08-13',23,3,0,0,1.41,0.42,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (219,'2025-08-13',23,1,0.0278,17.62,0.489836,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (220,'2025-09-03',17,1,539.96,1.852,1000.00592,0,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (221,'2025-09-03',13,1,996.71,1.0033,999.999143,0,-1000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (222,'2025-09-03',12,1,6773.3,2.1128,14310.62824,214.66,-14525.28824,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (223,'2025-09-11',23,3,0,0,0.54,0.05,0.49,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (224,'2025-09-12',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (225,'2025-09-12',23,3,0,0,1.42,0.42,1,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (226,'2025-09-12',23,1,0.0275,17.81,0.489775,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (227,'2025-09-22',11,1,6810.13,2.9368,19999.989784,0,-20000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (228,'2025-09-22',14,1,9660.52,1.0339,9988.011628,11.99,-10000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (229,'2025-09-23',16,1,933.97,1.1806,1102.644982,0,-1102.644982,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (230,'2025-09-23',16,1,745.95,1.1806,880.66857,0,-880.66857,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (231,'2025-09-25',27,3,0,0,4.88,1.47,3.41,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (232,'2025-09-25',9,1,22200.26,2.2511,49975.005286,24.99,-50000,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (233,'2025-10-10',23,3,0,0,0.54,0.05,0.49,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (234,'2025-10-13',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (235,'2025-10-13',23,3,0,0,1.41,0.42,0.99,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (236,'2025-10-13',23,1,0.0289,16.93,0.489277,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (237,'2025-10-17',7,1,3100,9.543,29583.3,1.48,-29584.78,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (238,'2025-11-04',26,3,0,0,1.83,0.54,1.29,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (239,'2025-11-04',24,3,0,0,0.69,0.2,0.49,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (240,'2025-11-13',23,3,0,0,0.53,0.05,0.48,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (241,'2025-11-14',25,3,0,0,0.57,0.17,0.4,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (242,'2025-11-14',23,3,0,0,1.37,0.41,0.96,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (243,'2025-11-14',23,1,0.028,17.45,0.4886,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (244,'2025-12-10',23,3,0,0,0.52,0.05,0.47,11,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (245,'2025-12-11',25,3,0,0,0.57,0.05,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (246,'2025-12-11',23,3,0,0,1.35,0.14,1.21,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (247,'2025-12-11',23,1,0.0272,17.6,0.47872,0,0,10,'股息再投资');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (248,'2025-12-13',3,1,6100,1.415,8631.5,0.43,-8631.93,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (249,'2025-12-13',4,1,10900,0.796,8676.4,0.43,-8676.83,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (250,'2025-12-24',6,1,300,1.433,429.9,0.1,-430,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (251,'2025-12-24',2,1,4500,1.19,5355,0.27,-5355.27,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (252,'2025-12-24',8,1,2000,1.155,2310,0.12,-2310.12,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (253,'2025-12-24',5,1,4500,1.532,6894,0.34,-6894.34,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (254,'2025-12-24',1,1,4200,1.245,5229,0.26,-5229.26,4,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (255,'2025-12-26',27,3,0,0,5.49,0.54,4.95,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (256,'2026-01-02',24,3,0,0,0.79,0.07,0.72,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (257,'2026-01-08',11,2,6810.13,3.532,24053.37916,0,24053.38,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (258,'2026-01-08',19,2,584.19,1.3423,784.158237,0,784.15,5,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (259,'2026-01-08',20,2,168.11,2.8297,475.700867,0,475.700867,5,'转015453');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (260,'2026-01-08',17,2,539.96,1.7681,954.703276,0,954.703276,5,'转000968');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (261,'2026-01-08',28,1,322.49,1.4729,474.995521,0.71,-475.7,5,'由004813转');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (262,'2026-01-08',13,1,980.49,0.9737,954.703113,0,-954.7,5,'由017512转');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (263,'2026-01-08',15,2,1344.04,1.465,1969.0186,0,1969.0186,5,'转020156');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (264,'2026-01-08',29,1,1721.02,1.1441,1969.018982,0,-1969.0186,5,'由519710转');
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (265,'2026-01-08',25,3,0,0,0.57,0.05,0.52,9,NULL);
INSERT INTO "fund_transactions" ("id","transaction_date","fund_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (266,'2026-01-08',23,3,0,0,1.35,0.14,1.21,9,NULL);
INSERT INTO "market" ("id","code","name","desc") VALUES (1,'SH','上海证券交易所','上海市场，代码以5、6开头');
INSERT INTO "market" ("id","code","name","desc") VALUES (2,'SZ','深圳证券交易所','深圳市场，代码以1、2开头');
INSERT INTO "market" ("id","code","name","desc") VALUES (3,'BJ','北京证券交易所','北京市场（REITs），代码以8开头');
INSERT INTO "market" ("id","code","name","desc") VALUES (4,'OF','场外市场','场外基金，通过基金公司直接申购赎回');
INSERT INTO "market" ("id","code","name","desc") VALUES (5,'US','美国市场','美国市场股票或ETF');
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (1,1,'601398','工商银行',1,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (2,5,'AAPL','苹果(APPLE)',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (3,5,'AMD','超威半导体(AMD)',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (4,5,'KO','可口可乐(COCA COLA)',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (5,5,'NVDA','英伟达(NVIDIA)',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (6,5,'IBKR','盈透证券(INTERACTIVE BROKERS)',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (7,5,'PLTR','PALANTIR TECHNOLOGIES',2,1,5,1);
INSERT INTO "stock" ("id","market_id","code","name","currency_id","four_type_money_id","class_assets_id","type_assets_id") VALUES (8,2,'002407','多氟多',1,3,5,1);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (1,1,'2026-01-13',7.71);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (2,2,'2026-01-13',259.37);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (3,3,'2026-01-13',203.17);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (4,4,'2026-01-13',70.51);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (5,5,'2026-01-13',184.86);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (6,6,'2026-01-13',70.47);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (7,7,'2026-01-13',177.49);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (8,8,'2026-01-13',32.93);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (50,1,'2026-01-22',7.27);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (51,2,'2026-01-22',248.35);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (52,3,'2026-01-22',253.73);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (53,4,'2026-01-22',71.87);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (54,5,'2026-01-22',184.84);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (55,6,'2026-01-22',77.21);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (56,7,'2026-01-22',165.9);
INSERT INTO "stock_net_asset_value" ("id","stock_id","date","nav") VALUES (57,8,'2026-01-22',31.31);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (1,'2020-09-01',2,1,10,131.7,1317,1.82,-1318.82,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (2,'2020-11-13',2,3,0,0,2.05,0.61,1.44,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (3,'2020-11-24',2,1,13,114.43,1487.59,1.83,-1489.42,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (4,'2021-02-12',2,3,0,0,4.71,0.47,4.24,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (5,'2021-05-14',2,3,0,0,5.06,0.51,4.55,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (6,'2021-08-13',2,3,0,0,5.06,0.51,4.55,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (7,'2021-11-15',2,3,0,0,5.06,0.51,4.55,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (8,'2022-02-11',2,3,0,0,5.06,0.51,4.55,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (9,'2022-05-13',2,3,0,0,5.29,0.51,4.78,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (10,'2022-08-12',2,3,0,0,5.29,0.53,4.76,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (11,'2022-11-11',2,3,0,0,5.29,0.53,4.76,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (12,'2023-02-17',2,3,0,0,5.29,0.53,4.76,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (13,'2023-05-19',2,3,0,0,5.52,0.56,4.96,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (14,'2023-08-18',2,3,0,0,5.52,0.56,4.96,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (15,'2023-11-17',2,3,0,0,5.52,0.56,4.96,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (16,'2024-02-15',2,2,3,183.4,550.2,1.82,548.38,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (17,'2024-02-16',2,3,0,0,5.52,0.56,4.96,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (18,'2024-02-23',3,1,3,175.15,525.45,1.8,-527.25,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (19,'2024-02-26',4,1,4,61.0887,244.35,1.8,-246.1548,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (20,'2024-02-26',2,2,10,181.585,1815.85,1.84,1814.01,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (21,'2024-02-26',5,1,20,79.717,1594.34,1.8,-1596.14,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (22,'2024-03-28',5,3,0,0,0.08,0,0.08,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (23,'2024-04-03',4,3,0,0,1.94,0.2,1.74,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (24,'2024-05-17',2,3,0,0,2.5,0.25,2.25,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (25,'2024-07-01',5,3,0,0,0.2,0.02,0.18,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (26,'2024-07-02',4,3,0,0,1.95,0.2,1.75,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (27,'2024-08-16',2,3,0,0,2.5,0.25,2.25,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (28,'2024-10-02',4,3,0,0,1.95,0.2,1.75,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (29,'2024-10-04',5,3,0,0,0.2,0.02,0.18,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (30,'2024-11-15',2,3,0,0,2.5,0.25,2.25,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (31,'2024-12-17',4,3,0,0,1.95,0.2,1.75,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (32,'2024-12-30',5,3,0,0,0.2,0.02,0.18,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (33,'2025-02-14',2,3,0,0,2.5,0.25,2.25,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (34,'2025-03-19',6,1,0.0336,44.537827381,1.5,0,-1.4964710000016,10,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (35,'2025-04-02',4,3,0,0,2.04,0.2,1.84,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (36,'2025-04-04',5,3,0,0,0.2,0.02,0.18,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (37,'2025-05-12',7,1,8,116.72,933.76,0,-933.76,11,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (38,'2025-05-16',2,3,0,0,2.6,0.79,1.81,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (39,'2025-07-02',4,3,0,0,2.04,0.62,1.42,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (40,'2025-07-08',5,3,0,0,0.2,0.06,0.14,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (41,'2025-08-18',2,3,0,0,2.6,0.79,1.81,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (42,'2025-10-02',4,3,0,0,2.04,0.62,1.42,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (43,'2025-10-03',5,3,0,0,0.2,0.06,0.14,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (44,'2025-10-31',1,1,800,7.75,6200,5.06,-6205.06,4,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (45,'2025-11-12',1,2,400,8.3,3320,6.69,3313.31,4,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (46,'2025-11-14',2,3,0,0,2.6,0.79,1.81,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (47,'2025-12-12',1,3,0,0,56.56,0,56.56,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (48,'2025-12-16',4,3,0,0,2.04,0.2,1.84,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (49,'2025-12-29',5,3,0,0,0.2,0.02,0.18,9,NULL);
INSERT INTO "stock_transactions" ("id","transaction_date","stock_id","type_transction_id","quantity","price","turnover","fee","transaction_amount","account_id","notes") VALUES (50,'2026-01-08',8,1,300,32.82,9846,5,-9851,4,NULL);
INSERT INTO "type_assets" ("id","name") VALUES (1,'股票');
INSERT INTO "type_assets" ("id","name") VALUES (2,'基金');
INSERT INTO "type_assets" ("id","name") VALUES (3,'基金顾投');
INSERT INTO "type_assets" ("id","name") VALUES (4,'理财存款');
INSERT INTO "type_assets" ("id","name") VALUES (5,'保险');
INSERT INTO "type_assets" ("id","name") VALUES (6,'现金及等价物');
INSERT INTO "type_transaction" ("id","name") VALUES (1,'买入');
INSERT INTO "type_transaction" ("id","name") VALUES (2,'卖出');
INSERT INTO "type_transaction" ("id","name") VALUES (3,'分红/利息');
INSERT INTO "type_transaction" ("id","name") VALUES (4,'保费缴纳');
INSERT INTO "type_transaction" ("id","name") VALUES (5,'现金价值提取');
COMMIT;
