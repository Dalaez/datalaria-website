---
title: "Building My Digital 'Swiss Army Knife': A Custom Unit Converter with AI"
date: 2025-09-21
draft: False
categories: ["Projects", "Tools"]
tags: ["gemini", "ai", "web development", "unit converter", "html", "css", "javascript", "engineering"]
image: conversor_universal_pro.png
description: "A practical case study of how I used Gemini Canvas to develop a multi-category unit conversion web application from scratch, tailored to my professional needs."
summary: "Tired of dusting off long-forgotten knowledge or relying on various generic online converters, I decided to create my own with the help of Gemini's AI. I'll walk you through the process and explain the science behind each conversion, from energy to radio frequency."
---

In any technical or engineering discipline, our daily work is filled with small but constant unit conversion tasks. We switch from Pascals to PSI, Kilowatts to Horsepower, Gigabytes to Terabytes, or from frequency to wavelength. In my university days, we had so-called *cheatsheets*, which we used to keep handy on our calculators, folders, or notebooks for daily use (not for exams, of course 😄). Now, in the professional world, with the proliferation of all kinds of apps and websites, it's no longer necessary to rely on these resources, as we have a multitude of options available that allow us to quickly look up any conversion or unit, no matter how obscure.

However, given the overwhelming number of options and this being such a recurrent and necessary task, I set myself a challenge: could I create my own unit converter? One that was fast, clean, visually appealing, and, above all, **a living project**—a kind of "digital Swiss army knife" that I could expand over time according to my personal and professional needs. The answer, as in other blog projects, I found in AI. This post describes my own unit converter, covering its development from scratch with the support of **Gemini's Canvas** feature to create a web application with multiple pages and categories.

![Conceptual image of the Universal Converter Pro application](knife_conversor.png)

### The Process: From Idea to Conception

The goal was to create a modern, intuitive web application with clear navigation by categories, and that was smooth and easy to use. Instead of starting to write code from scratch, I began a conversation with Gemini, describing my vision:

> "Create the structure for a multi-page HTML web application. The application will be a format and unit converter. The main page should display cards for the categories: Dimension, Energy, Time, Mechanics, Computing, and Radio Frequency with basic conversions. Each card should link to a dedicated conversion page for the corresponding category from a homepage where, in addition to the navigation cards for each category, there should be a format converter for the '.' and ',' symbols for thousands and decimals in numbers."

Gemini's Canvas feature allowed me to see in real-time how the AI generated not just the code, but the complete project structure. After the initial draft and a couple of additional iterations focused on refining the design and fine-tuning the units, a first operational version of the application came to life: [My unit conversion application](https://dalaez.github.io/conversor-app/)

### A Look at the Categories and Their Units

What makes a tool like this useful is understanding **what we are converting**. That's why the "Universal Converter Pro" not only calculates but also aims to be educational. These are the initial categories and the science behind their units:

![Universal Converter Pro Homepage Image](conversor-app.png)

#### 1. Dimension: Measuring the Space Around Us

![Conceptual image of the Dimension Converter Page](dimension.png)

This category groups the fundamental measures of physical space.

* **Length:**
    * **What is it?** It is the measure of one dimension, the distance between two points.
    * **How is it calculated?** All conversions are calculated using the **meter (m)** as the reference unit. The formula converts the initial value to meters and then to the final unit.

* **Area:**
    * **What is it?** It is the measure of a two-dimensional surface.
    * **How is it calculated?** Similarly, the calculation is standardized using the **square meter (m²)** as the base unit.

* **Volume:**
    * **What is it?** It is the measure of the space an object occupies in three dimensions.
    * **How is it calculated?** The base unit for volume in the application is the **liter (l)**, making it easy to convert between metric units and others like gallons or cups.

#### 2. Energy: The Capacity to Do Work

![Conceptual image of the Energy Converter Page](energy.png)

Here we group the units that describe how energy is transferred and used.

* **Energy:**
    * **What is it?** It is the capacity of a system to perform work.
    * **How is it calculated?** The **Joule (J)** is the base unit of the International System. From it, conversions to calories, watt-hours, etc., are performed.

* **Power:**
    * **What is it?** It is the rate at which energy is transferred or work is done. It's not the same to have energy as to be able to use it quickly.
    * **How is it calculated?** The base unit is the **Watt (W)**, which is equivalent to one Joule per second.

* **Temperature:**
    * **What is it?** It is a measure of the thermal energy or heat of a body.
    * **How is it calculated?** Unlike others, temperature does not use a simple conversion factor. The application uses specific formulas, always converting the input to **degrees Celsius (°C)** as an intermediate step to then calculate the output unit (Fahrenheit or Kelvin).

#### 3. Computing: The World of Bits and Bytes

![Conceptual image of the Data Converter Page](data.png)

The units that define our digital world.

* **Data Storage:**
    * **What is it?** It measures the capacity to store digital information.
    * **How is it calculated?** The fundamental unit is the **Byte (B)**. It is important to note that in computing, multiples are not decimal (x1000), but binary (x1024). Thus, 1 Kilobyte is 1024 Bytes.

* **Bandwidth:**
    * **What is it?** It measures the data transfer rate in a network.
    * **How is it calculated?** Its base unit is **bits per second (bps)**. In this case, the multiples are decimal (kbps, mbps, gbps), as they refer to transmission speed, not storage.

#### 4. Time: Our Most Precious Dimension

![Conceptual image of the Time Converter Page](time.png)

Although it seems simple, time conversion is fundamental in many calculations.

* **Time:**
    * **What is it?** It is the magnitude that measures the duration or separation of events.
    * **How is it calculated?** All units are converted to the base unit, the **second (s)**, to then calculate the final value in minutes, hours, days, etc.

#### 5. Mechanics: The Forces that Move the World

![Conceptual image of the Mechanics Converter Page](mechanics.png)

This category is key in engineering and physics.

* **Mass:**
    * **What is it?** It is the measure of the amount of matter in a body. It should not be confused with weight, which is the force exerted by gravity on that mass.
    * **How is it calculated?** The base unit is the **Kilogram (kg)**.

* **Force:**
    * **What is it?** It is any interaction that, unopposed, changes the motion of an object.
    * **How is it calculated?** The **Newton (N)** is used as the base unit, defined as the force required to provide an acceleration of 1 m/s² to an object of 1 kg of mass.

* **Pressure:**
    * **What is it?** It is the force applied perpendicularly to a surface.
    * **How is it calculated?** The base unit is the **Pascal (Pa)**, which is equal to one Newton per square meter (N/m²).

#### 6. Radio Frequency: The Invisible Spectrum

![Conceptual image of the Radiofrequency Converter Page](radiofrequency.png)

Fundamental for telecommunications.

* **Frequency:**
    * **What is it?** It is the number of repetitions of a periodic phenomenon per unit of time. In waves, it is the number of cycles per second.
    * **How is it calculated?** Its base unit is the **Hertz (Hz)**, which is equivalent to one cycle per second.

* **Frequency to Wavelength:**
    * **What is it?** This is a special conversion that relates the frequency of an electromagnetic wave to its wavelength (the distance between two crests of the wave).
    * **How is it calculated?** It is not a direct conversion but uses a physical formula: **λ = c / f**, where **λ** is the wavelength, **f** is the frequency, and **c** is the constant of the speed of light (299,792,458 m/s). The application converts the frequency to Hz, calculates the wavelength in meters, and then converts it to the desired length unit.

### Conclusion: More Than a Tool, a Living Project

The "Universal Converter Pro" is the perfect example of how, thanks to AI, ideas and resources of great utility for our personal or professional daily life can be materialized. The process, in this case guided by Gemini Canvas, was incredibly agile, and the result is an application that not only solves my daily needs but also serves as a learning platform.

My goal is to continue expanding it with new categories and units as the needs arise. This is the new era of personal software development: we no longer depend on generic tools but have the power to build our own custom solutions, with an AI copilot that translates our ideas into functional code.

---

#### Sources and Resources:
* **Gemini**: [Official Gemini page to try its Canvas functionality](https-gemini.google.com/app)
* **App's GitHub Page**: [My unit conversion application](https://dalaez.github.io/conversor-app/)