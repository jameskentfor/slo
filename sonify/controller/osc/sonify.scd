// Sonify — SuperCollider integration
// Run headlessly: sclang sonify.scd
//
// Requires scsynth to be able to open an audio device. On a headless server,
// start JACK first (e.g. jackd -d dummy) or use a virtual audio sink.

s.options.device = "pulse";

s.waitForBoot {

    // Define the synth: filtered saw wave with controllable cutoff and pan.
    SynthDef(\sonify, {
        arg cutoff = 1000, pan = 0, amp = 0.3;
        var sig = Saw.ar(110);
        sig = RLPF.ar(sig, cutoff, 0.3);
        sig = Pan2.ar(sig, pan, amp);
        Out.ar(0, sig);
    }).add;

    // Wait for the SynthDef to finish loading on the server before instantiating.
    s.sync;

    ~synth = Synth(\sonify);
    "Sonify synth running.".postln;

    // OSC responders
    // Sonify sends normalized values in [0.0, 1.0]; map to useful audio ranges.
    //
    //   /synth/filter_cutoff  — moon_phase    → filter frequency 200–8000 Hz
    //   /synth/pan            — moon_illumination → stereo pan -1.0 to 1.0

    OSCdef(\filter_cutoff, { |msg|
        var norm = msg[1];
        var freq = norm.linlin(0.0, 1.0, 200, 8000);
        ~synth.set(\cutoff, freq);
    }, '/synth/filter_cutoff');

    OSCdef(\pan, { |msg|
        var norm = msg[1];
        var pos = norm.linlin(0.0, 1.0, -1.0, 1.0);
        ~synth.set(\pan, pos);
    }, '/synth/pan');

    "OSC responders registered. Listening on port 57120.".postln;
};
