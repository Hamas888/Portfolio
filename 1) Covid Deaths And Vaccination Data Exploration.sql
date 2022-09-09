--Covid Deaths table

select *
from Projects..covid_deaths
order by 3,4;

--Covid Vaccinations table

select * 
from Projects..covid_vaccinations 
order by 3,4;

----------------------------------------------------------------------------------------------------------------------------------
--Exploaring Covid Deaths Data

select location, date, total_cases, new_cases, total_deaths, population
from Projects..covid_deaths
order by 1,2;

--Looking  at Total Cases vs Total Deaths
--Shows likehhod of dying if you got covid in pakistan
 
select location, date, total_cases,  total_deaths, round((total_deaths/total_cases)*100, 2) as death_percentage
from Projects..covid_deaths
where location = 'Pakistan'
order by 1,2;

--Looking  at Total Cases vs Population
--Shows what percentage of population got covid in pakistan

select location, date, total_cases,  population, 
round((total_cases/population)*100, 2) as infected_population_percentage
from Projects..covid_deaths
where location = 'Pakistan'
order by 1,2;

--Looking at Counteries with highest infection rate compared to Population

select location, population, max( total_cases) as highest_infection_count,
max(round((total_cases/population)*100, 2)) as infected_population_percentage
from Projects..covid_deaths
where continent is not null
group by location, population
order by 4 desc;

--Showing Countries with highest Death Count per Population

select location, population ,max(cast(total_deaths as int)) as highest_death_count
from Projects..covid_deaths
where continent is not null
group by location, population
order by 3 desc;

--Showing Continents with highest Death Count per Population

select continent, max(cast(total_deaths as int)) as highest_death_count
from Projects..covid_deaths
--where continent is not null
group by continent
order by 2 desc;

--Looking New Cases vs New Deaths 
--Showing drop down in death percentage per year

select  year(date) as year, sum(new_cases) as total_new_cases ,sum(cast(new_deaths as int)) as total_new_deaths,
round(sum(cast(new_deaths as int))/sum(new_cases)*100, 2) as death_percentage
from Projects..covid_deaths
where continent is not null
group by year(date)
order by 4 desc;

----------------------------------------------------------------------------------------------------------------------------------
--Exploaring Covid Vaccinations Data

--Looking at Total Population vs Vaccinations

--Creating CTE
with popvsvac 
as
(
select cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
sum(convert(bigint,cv.new_vaccinations)) over (partition by cd.location order by cd.location, cd.date)
as rolling_vaccinated_people_count
from Projects..covid_deaths as cd join Projects..covid_vaccinations as cv
on cd.location = cv.location and cd.date = cv.date 
where cd.continent is not null
)
 
--Showing percentage of vaccinated People 
--Percentage over 100 mean double or triple dose vaccinations

select location, population, max(rolling_vaccinated_people_count) as vaccinated_people_count,
round((max(rolling_vaccinated_people_count)/population)*100, 2) as vaccination_percentage
from popvsvac
group by location,population
order by 4 desc;

--Showing percentage of vaccinated People in pakistan

--Creating View of Population vs Vaccinations

drop view  if exists population_vs_vaccination ; 

create view population_vs_vaccination 
as
select cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
sum(convert(bigint,cv.new_vaccinations)) over (partition by cd.location order by cd.location, cd.date)
as rolling_vaccinated_people_count
from Projects..covid_deaths as cd join Projects..covid_vaccinations as cv
on cd.location = cv.location and cd.date = cv.date 
where cd.continent is not null;

select location, population, max(rolling_vaccinated_people_count) as vaccinated_people_count,
round((max(rolling_vaccinated_people_count)/population)*100, 2) as vaccination_percentage
from population_vs_vaccination
where location = 'Pakistan'
group by location,population;
