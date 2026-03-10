#![no_std]
#![no_main]

mod fmt;

#[cfg(not(feature = "defmt"))]
use panic_halt as _;
#[cfg(feature = "defmt")]
use {defmt_rtt as _, panic_probe as _};

use embassy_executor::Spawner;
use embassy_time::{Duration, Timer};
use defmt::info;

const SRAM4_START: usize = 0x38000000;
const SRAM4_SIZE: usize = 16 * 1024;
const BOTTOM_HALF_SIZE: usize = SRAM4_SIZE / 2;
const BYTES_PER_LINE: usize = 16;

#[embassy_executor::main]
async fn main(_spawner: Spawner) {
    let _p = embassy_stm32::init(Default::default());

    // Wait for the debugger
    Timer::after_millis(500).await;
    defmt::flush();

    defmt::info!("--- DATA_START ---");

    let mut addr = SRAM4_START + BOTTOM_HALF_SIZE;
    while addr < SRAM4_START + SRAM4_SIZE {
        let mut line = [0u8; BYTES_PER_LINE];
        // Read a line of memory
        for i in 0..BYTES_PER_LINE {
            if addr + i < SRAM4_START + SRAM4_SIZE {
                line[i] = unsafe { core::ptr::read_volatile((addr + i) as *const u8) };
            }
        }

        // Log the line of data to the host computer
        info!("{:08x}: {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x}",
              addr,
              line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7],
              line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15]);
        addr += BYTES_PER_LINE;

        // Small delay helps combat flooding
        Timer::after(Duration::from_micros(100)).await;
    }

    info!("--- DATA_END ---");
}
