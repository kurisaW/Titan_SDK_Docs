# RA8P1 Titan Board 开发板  IST8310 示例说明

**中文** | [**English**](./README_EN.md)

## 简介

本例程主要介绍了如何在 Titan Board 上使用 RT-Thread 的 IIC 框架与 IST8310 磁力计模块通信。

## 硬件说明

Titan Board 使用 IIC2 与 IST8310 通信；

![image-20250730150751353](figures/image-20250730150751353.png)

## FSP配置说明

新建 stacks 选择 r_iic_master 并配置 IIC2 配置信息如下：

![image-20250730150953970](figures/image-20250730150953970.png)

## RT-Thread Settings 配置

在配置中打开 RT-Thread 的 IIC 驱动框架与 IST8310 的驱动软件包；

![image-20250730151140705](figures/image-20250730151140705.png)

![image-20250730151319214](figures/image-20250730151319214.png)

## 示例工程说明

基于 IST8310 的驱动软件包实现对磁力计的数据通信。

```c
/*
* Copyright (c) 2006-2025, RT-Thread Development Team
*
* SPDX-License-Identifier: Apache-2.0
*
* Change Logs:
* Date           Author        Notes
* 2025-06-13     kurisaW       first version
*/

#include <rtthread.h>
#include "ist8310.h"

static void ist8310_entry()
{
    ist8310_device_t dev = ist8310_init(IST8310_SAMPLE_I2C_DEV_NAME);
    if (dev == RT_NULL) {
        rt_kprintf("IST8310 init failed\n");
        return;
    }

    /* 设置磁偏角（根据实际位置设置） */
    ist8310_set_declination(dev, 0.15f);  /* 例如：0.15弧度 */

    while (1)
    {
        ist8310_data_t data;
        if (ist8310_read_magnetometer(dev, &data) == RT_EOK)
        {
            rt_kprintf("Magnetic: X=%.2f µT, Y=%.2f µT, Z=%.2f µT\n", data.x, data.y, data.z);
        }

        float heading = ist8310_read_heading(dev);
        rt_kprintf("Heading: %.2f°\n", heading);

        rt_thread_mdelay(1000);
    }
}

void ist8310_app()
{
    rt_thread_t ist8310 = rt_thread_create("ist8310", ist8310_entry, RT_NULL, 2048, 20, 10);
    if(ist8310 != RT_NULL)
    {
        rt_thread_startup(ist8310);
    }

    return;
}
MSH_CMD_EXPORT(ist8310_app, IST8310 app);
```

## 编译&下载

* RT-Thread Studio：在RT-Thread Studio 的包管理器中下载 Titan Board 资源包，然后创建新工程，执行编译。

编译完成后，将开发板的 Jlink 接口与 PC 机连接，然后将固件下载至开发板。

##  运行效果

串口终端输入 ist8310_app 指令： 

![PixPin_2025-07-28_09-21-40](figures/PixPin_2025-07-28_09-21-40.png)
