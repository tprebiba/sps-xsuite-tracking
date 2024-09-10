/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.cngs;

import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the CNGS Beam line transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class CngsModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("CNGS");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("cngs");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("tt41.new-naming.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] { "round.30m.str" };

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll(".str", "");

            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

        /* NOTE: sequenceName must correspond to the name in .seq - file! */
        SequenceDefinitionImpl tt41 = new SequenceDefinitionImpl("tt41", BeamFactory.createDefaultCngsBeam());
        modelDefinition.setDefaultSequenceDefinition(tt41);
        RangeDefinitionImpl tt41range = new RangeDefinitionImpl(tt41, "ALL", createCngsTwiss());
        tt41.setDefaultRangeDefinition(tt41range);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline Ti2
     */
    private final TwissInitialConditionsImpl createCngsTwiss() {
        TwissInitialConditionsImpl twiss = new TwissInitialConditionsImpl("tt41-twiss");

        /*
         * values from Jorg
         * 
         * ! ! initial conditions for standard SPS WP - no qsplit - jun06
         * 
         * betxin = 16.85821; alfxin = 0.442003; dxin = -0.246627; dpxin = 0.0054976; betyin = 123.7823; alfyin =
         * -3.453686; dyin = 0; dpyin = 0;
         */

        twiss.setDeltap(0.0);
        twiss.setBetx(16.85821);
        twiss.setAlfx(0.442003);
        twiss.setDx(-0.246627);
        twiss.setDpx(0.0054976);
        twiss.setBety(123.7823);
        twiss.setAlfy(-3.453686);
        twiss.setDy(0.0);
        twiss.setDpy(0.0);

        return twiss;

    }

}
