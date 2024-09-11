/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt2tt10;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.filter.RegexNameFilter;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.domain.types.enums.JMadPlane;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the TI2 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class Tt2Tt10ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT2TT10");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt2tt10");
        offsets.setRepositoryOffset("");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("init0.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/elements/tt2_2011.ele",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/elements/tt10_2011.ele",
                ModelFileLocation.REPOSITORY));

        modelDefinition.addInitFile(new CallableModelFileImpl("init1.madx", ModelFileLocation.RESOURCE));

        modelDefinition.addInitFile(new CallableModelFileImpl("tt2_2011.seq", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/aperture/tt2_2011.dbx",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/sequence/tt10_2011.seq",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/aperture/tt10_2011.dbx",
                ModelFileLocation.REPOSITORY));

        /*
         * SPS
         */

        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/elements/sps2008.ele",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/aperture/aperturedb_1_2008.dbx",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/strength/elements.str",
                ModelFileLocation.REPOSITORY));

        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/aperture/aperturedb_2_2008.dbx",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/sequence/sps2008.seq",
                ModelFileLocation.REPOSITORY));
        modelDefinition.addInitFile(new CallableModelFileImpl("sps/2008/aperture/aperturedb_3_2008.dbx",
                ModelFileLocation.REPOSITORY));

        modelDefinition.addInitFile(new CallableModelFileImpl("compose-sequences.madx", ModelFileLocation.RESOURCE));

        modelDefinition.addInitFile(new CallableModelFileImpl("lhc_beam_DPPeqBucketheight.beamx",
                ModelFileLocation.RESOURCE));

        OpticsDefinition nominalLhcOptic = new OpticsDefinitionImpl("Nominal LHC Optics", new ModelFile[] {
                new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/strength/tt2_fe_26_2011.str",
                        ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("ps/cps/TransLines/PS-SPS/2011/strength/tt10_fe_26_2011.str",
                        ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("sps/2008/strength/lhc_newwp_2008.str", ModelFileLocation.REPOSITORY,
                        ParseType.STRENGTHS) });
        modelDefinition.addOpticsDefinition(nominalLhcOptic);

        OpticsDefinition q20Optic = new OpticsDefinitionImpl("Q=20 LHC Optics", new ModelFile[] {
                new CallableModelFileImpl("TT2TT10forQ20.str", ModelFileLocation.RESOURCE, ParseType.STRENGTHS),
                new CallableModelFileImpl("SPS_Q20.str", ModelFileLocation.RESOURCE, ParseType.STRENGTHS) });
        modelDefinition.addOpticsDefinition(q20Optic);

        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

        /* NOTE: sequenceName must correspond to the name in .seq - file! */

        SequenceDefinitionImpl tt2tt10 = new SequenceDefinitionImpl("tt2tt10", null);
        modelDefinition.setDefaultSequenceDefinition(tt2tt10);
        RangeDefinitionImpl tt2tt10range = new RangeDefinitionImpl(tt2tt10, "ALL", createTt2Twiss());
        tt2tt10.setDefaultRangeDefinition(tt2tt10range);

        SequenceDefinitionImpl tt2 = new SequenceDefinitionImpl("tt2", null);
        modelDefinition.addSequenceDefinition(tt2);
        RangeDefinitionImpl tt2range = new RangeDefinitionImpl(tt2, "ALL", createTt2Twiss());
        tt2.setDefaultRangeDefinition(tt2range);

        SequenceDefinitionImpl tt2tt10sps = new SequenceDefinitionImpl("tt2tt10sps", null);
        modelDefinition.addSequenceDefinition(tt2tt10sps);
        RangeDefinitionImpl tt2tt10spsrange = new RangeDefinitionImpl(tt2tt10sps, "ALL", createTt2Twiss());
        tt2tt10sps.setDefaultRangeDefinition(tt2tt10spsrange);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline Ti2
     */
    private final TwissInitialConditionsImpl createTt2Twiss() {
        TwissInitialConditionsImpl twiss = new TwissInitialConditionsImpl("tt2-twiss");

        /*
         * 
         * ! tt2_fe_26_2010.inp ! ! initial twiss parameters for TT2 @ 26 GeV/c fast extraction ! These are the values
         * for LHC beam when the quadrupoles ! QKE58 inside the PS are NOT used for the extraction. ! ! new
         * measurements, QKE58 off, July 2007 (E.Benedetto) ! The measurements have been done without bunch rotation
         * from the PS
         * 
         * BETX0 := 26.1431; ALFX0 := -2.2287; MUX0 := 0.000000000000; BETY0 := 10.883; ALFY0 := 0.762; MUY0 :=
         * 0.000000000000; X0 := 0.000000000000; PX0 := 0.000000000000; Y0 := 0.000000000000; PY0 := 0.000000000000; T0
         * := 0.000000000000; PT0 := 0.000000000000; DX0 := 3.0414; DPX0 := 0.25256; DY0 := 0.024; DPY0 := -0.014;
         * 
         * 
         * return;
         */

        twiss.setDeltap(0.0);
        twiss.setBetx(26.1431);
        twiss.setAlfx(-2.2287);
        twiss.setDx(3.0414);
        twiss.setDpx(0.25256);
        twiss.setBety(10.883);
        twiss.setAlfy(0.762);
        twiss.setDy(0.024);
        twiss.setDpy(-0.014);

        return twiss;

    }

}
