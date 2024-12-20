/*
 * Copyright (c) 2020 Libre Solar Technologies GmbH
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <zephyr/logging/log.h>
#include <dk_buttons_and_leds.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include "adc.h"
#include <zephyr/device.h>
#include <zephyr/devicetree.h>

#include "confusion.h"
//#include "neuroverkonKertoimet.h"



#define USER_LED1         	 	DK_LED1
#define USER_LED2          		DK_LED2
#define USER_LED3               DK_LED3
#define USER_LED4               DK_LED4

#define USER_BUTTON_1           DK_BTN1_MSK
#define USER_BUTTON_2           DK_BTN2_MSK
#define USER_BUTTON_3           DK_BTN3_MSK
#define USER_BUTTON_4           DK_BTN4_MSK

#define DEBUG 0  // 0 = changes direction when button 3 is pressed
                 // 1 = fake 100 measurements done to each 6 directions when 3 pressed.
static int direction = -1;	// 0 = x direction high
							// 1 = x directon low	
							// 2 = y direction high
							// 3 = y direction low
							// 4 = z direction high
							// 5 = z direction low
                				 

LOG_MODULE_REGISTER(MAIN, LOG_LEVEL_INF);

int state = 0; // 0 = k-means, 1 = neural network

static void button_changed(uint32_t button_state, uint32_t has_changed)
{
	//printk("button_state = %d\n",button_state);
	//printk("has_changed = %d\n",has_changed);
	if ((has_changed & USER_BUTTON_1) && (button_state & USER_BUTTON_1)) 
	{
		printk("Button 1 down, changing current state:\n");
		if(state == 0)
		{
			state = 1;
			printk("Classification is done with neural network\n");
		}
		else
		{
			state = 0;
			printk("Classification is done with k-means\n");
		}
		//printk("Button 1 down, printing current Confusion Matrix\n");
		//printConfusionMatrix();
	}

	if ((has_changed & USER_BUTTON_2) && (button_state & USER_BUTTON_2)) 
	{
		printk("Button 2 down, resetting confusion matrix\n");
		resetConfusionMatrix(state);
		printConfusionMatrix();
	}		
	
	if ((has_changed & USER_BUTTON_3) && (button_state & USER_BUTTON_3)) 
	{
		printk("Button 3 down, making fake 100 meas or one real meas depending on DEBUG state\n");
		#if DEBUG
		direction = 0;
		makeHundredFakeClassifications();
		printConfusionMatrix();
		#else
        direction = (direction +1)%6;
		switch (direction)
		{
		case 0:
			printk("Direction is now set x = low\n");
			break;
		case 1:
			printk("Direction is now set x = high\n");
			break;
		case 2:
			printk("Direction is now set y = low\n");
			break;
		case 3:
			printk("Direction is now set y = high\n");
			break;
		case 4:
			printk("Direction is now set z = low\n");
			break;
		case 5:
			printk("Direction is now set z = high\n");
			break;
		
		default:
		    printk("Wrong direction set!!!\n");
			break;
		}

		struct Measurement m = readADCValue();
		printk("x = %d,  y = %d,  z = %d\n",m.x,m.y,m.z);
		#endif
	}		

	if ((has_changed & USER_BUTTON_4) && (button_state & USER_BUTTON_4)) 
	{
		
		printk("button 4 down, one meas and classification with current direction =%d\n",direction);		

		for(int i = 0; i < 100; i++)
		{
			if(state == 0)
			{
				makeOneClassificationAndUpdateConfusionMatrix(direction);
			}
			else
			{
				makeClassificationWithNeuralNetwork(direction);
			}
		}
		printConfusionMatrix();
	}		
}

void main(void)
{
	
	
	/*	
	//Lasketaan softmax(a2) TOIMII
    float max = -__FLT_MAX__; //alustus pienimmällä float luvulla (=suurin negatiivinen luku)
    float sum = 0;

    // Etsitään suurin arvo
    for (int i = 0; i < w2Cols; i++) {
        if (a2[i] > max) {
            max = a2[i];
        }
    }

    // Vähennetään suurin arvo ja lasketaan e:n potenssiin x jokaiselle x:n alkiolle
    // Laske näiden summa
    for (int i = 0; i < w2Cols; i++) {
        a2[i] = exp(a2[i] - max);	//Vähennetään suurin arvo vektorista ennen e:n potenssiin laskemista (estää ylivuodon)
        sum = sum + a2[i];
    }

    // Jaa jokainen alkio summan arvolla
    for (int i = 0; i < w2Cols; i++) {
        a2[i] = a2[i] / sum;
    }
	printk("\nTulos softmax laskun jälkeen:\n");
	for (int i = 0; i < w2Cols; ++i) 
	{
		printk("%f ", a2[i]);
	}
	*/

	/*//RELU TESTI TOIMII
	int relu_array[] = {1, 2, 3, -1, -2, -3};
    int size = sizeof(relu_array) / sizeof(relu_array[0]);
	printk("Arrayn koko on %d",size);
    printk("Alkuperäinen taulukko:\n");
    for (int i = 0; i < size; ++i) {
        printk("%d ", relu_array[i]);
    }
    printk("\n");

    // Kutsutaan relu-funktiota
    relu(relu_array, size);

    printk("Muutettu taulukko:\n");
    for (int i = 0; i < size; ++i) {
        printk("%d ", relu_array[i]);
    }
    printk("\n");
	*/



	int err;
	err = dk_leds_init();
	if (err) {
		LOG_ERR("LEDs init failed (err %d)\n", err);
		return;
	}

	err = dk_buttons_init(button_changed);
	if (err) {
		printk("Cannot init buttons (err: %d)\n", err);
		return;
	}
	
	
	if(initializeADC() != 0)
	{
	printk("ADC initialization failed!");
	return;
	}

	while (1) 
	{
		//struct Measurement m = readADCValue();
		//printk("x = %d,  y = %d,  z = %d\n",m.x,m.y,m.z);
		if(state == 0)
		{
			k_sleep(K_MSEC(1000));
			
			dk_set_led_on(USER_LED1);
			dk_set_led_on(USER_LED2);
			dk_set_led_on(USER_LED3);
			dk_set_led_on(USER_LED4);
			
			k_sleep(K_MSEC(1000));
			
			dk_set_led_off(USER_LED1);
			dk_set_led_off(USER_LED2);
			dk_set_led_off(USER_LED3);
			dk_set_led_off(USER_LED4);
		}
		else
		{
			k_sleep(K_MSEC(100));
			
			dk_set_led_on(USER_LED1);
			k_sleep(K_MSEC(100));
			dk_set_led_off(USER_LED1);
			dk_set_led_on(USER_LED2);
			k_sleep(K_MSEC(100));
			dk_set_led_off(USER_LED2);
			dk_set_led_on(USER_LED3);
			k_sleep(K_MSEC(100));
			dk_set_led_off(USER_LED3);
			dk_set_led_on(USER_LED4);
			k_sleep(K_MSEC(100));
			dk_set_led_off(USER_LED4);
		}

	}
}


