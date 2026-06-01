-- ============================================================
-- FIX: Daj Analysis Services-u pristup SQL bazi
-- ============================================================
-- PROBLEM: OLAP servis (NT SERVICE\MSSQLServerOLAPService) 
-- nema permisiju da cita podatke iz ITKompanijaDW baze.
--
-- UPUTSTVO:
-- 1. SSMS -> Connect -> Database Engine -> .\SQLEXPRESS
-- 2. New Query -> zalepi ovo -> Execute (F5)
-- 3. Posle toga: vrati se na Analysis Services konekciju
-- 4. Desni klik na ITKompanijaDW_OLAP -> Process -> Process Full
-- ============================================================

USE [master]
GO
CREATE LOGIN [NT SERVICE\MSSQLServerOLAPService] FROM WINDOWS
GO
USE [ITKompanijaDW]
GO
CREATE USER [NT SERVICE\MSSQLServerOLAPService] FOR LOGIN [NT SERVICE\MSSQLServerOLAPService]
GO
EXEC sp_addrolemember 'db_datareader', 'NT SERVICE\MSSQLServerOLAPService'
GO
